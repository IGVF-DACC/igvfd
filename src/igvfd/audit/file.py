from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message,
    space_in_words
)


@audit_checker('File', frame='object')
def audit_upload_status(value, system):
    '''
    [
        {
            "audit_description": "Files are expected to be validated.",
            "audit_category": "upload status not validated",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "External files are expected to be validated.",
            "audit_category": "upload status not validated",
            "audit_level": "WARNING"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    upload_status = value.get('upload_status')
    if upload_status not in ['validated']:
        if value.get('external'):
            audit_level = 'WARNING'
            audit_message = get_audit_message(audit_upload_status, index=1)
        else:
            audit_level = 'ERROR'
            audit_message = get_audit_message(audit_upload_status, index=0)
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has `upload_status` {upload_status}.'
        )
        validation_error_detail = value.get('validation_error_detail')
        if upload_status == 'invalidated' and validation_error_detail:
            detail = f'{detail} Validation error detail: {validation_error_detail}.'
        yield AuditFailure(
            'upload status not validated',
            f'{detail} {audit_message.get("audit_description", "")}',
            level=audit_level
        )


@audit_checker('File', frame='object')
def audit_file_format_specifications(value, system):
    '''
    [
        {
            "audit_description": "File format specifications are excepted to be documents have type file format specification.",
            "audit_category": "inconsistent document type",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message = get_audit_message(audit_file_format_specifications)
    object_type = space_in_words(value['@type'][0]).capitalize()
    for document in value.get('file_format_specifications', []):
        document_object = system.get('request').embed(document)
        doc_type = document_object['document_type']
        if doc_type != 'file format specification':
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has `file_format_specification` {audit_link(path_to_text(document), document)} '
                f'with `document_type` {doc_type}.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('ModelFile', frame='object')
@audit_checker('SequenceFile', frame='object')
def audit_external_identifiers(value, system):
    '''
    [
        {
            "audit_description": "Externally hosted files are expected to have identifiers from external resources in dbxrefs.",
            "audit_category": "missing dbxrefs",
            "audit_level": "WARNING"
        }
    ]
    '''
    audit_message = get_audit_message(audit_external_identifiers)
    object_type = space_in_words(value['@type'][0]).capitalize()
    if value.get('externally_hosted'):
        if 'dbxrefs' not in value:
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} is externally hosted, '
                f'but does not have identifier(s) from an external resource listed in `dbxrefs`.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('ReferenceFile', frame='object')
def audit_external_reference_files(value, system):
    '''
    [
        {
            "audit_description": "Reference files uploaded from external resources are expected to have external identifiers in dbxrefs.",
            "audit_category": "missing dbxrefs",
            "audit_level": "WARNING"
        }
    ]
    '''
    audit_message = get_audit_message(audit_external_reference_files)
    object_type = space_in_words(value['@type'][0]).capitalize()
    if value.get('external'):
        if 'dbxrefs' not in value:
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} is an external file, '
                f'but does not have identifier(s) from an external resource listed in `dbxrefs`.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('IndexFile', frame='object')
def audit_index_files_derived_from(value, system):
    '''
    [
        {
            "audit_description": "The metadata of index files should match the metadata of the file they index.",
            "audit_category": "incorrect indexed file",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "Index files in tbi format are expected to have their corresponding tsv or vcf file in `derived_from`.",
            "audit_category": "incorrect indexed file",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message_mismatched_metadata = get_audit_message(audit_index_files_derived_from)[0]
    audit_message_tbi = get_audit_message(audit_index_files_derived_from)[1]
    object_type = space_in_words(value['@type'][0]).capitalize()
    # Check that metadata is consistent with the file it indexes.
    check_properties_list = ['content_type', 'assembly', 'filtered', 'redacted', 'transcriptome_annotation']
    inconsistent_properties_list = []
    derived_from_file = value.get('derived_from')
    derived_from_file_obj = system.get('request').embed(
        derived_from_file[0], '@@object?skip_calculated=true')
    for property in check_properties_list:
        if value.get(property) != derived_from_file_obj.get(property):
            inconsistent_properties_list.append(property)
        if inconsistent_properties_list:
            inconsistent_properties_str = ', '.join(inconsistent_properties_list)
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has '
                f'the following inconsistent properties with its indexed file in `derived_from`: '
                f'{inconsistent_properties_str}.'
            )
            yield AuditFailure(
                audit_message_mismatched_metadata.get('audit_category', ''),
                f'{detail} {audit_message_mismatched_metadata.get("audit_description", "")}',
                level=audit_message_mismatched_metadata.get('audit_level', '')
            )
    # For tbi files, check that the indexed file is of an expected file_format.
    # No need to check bai files, since Alignment Files can only be bams.
    if value['file_format'] == 'tbi':
        if derived_from_file_obj.get('file_format') not in ['tsv', 'vcf']:
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has a file of unexpected file format in `derived_from`.')
            yield AuditFailure(
                audit_message_tbi.get('audit_category', ''),
                f'{detail} {audit_message_tbi.get("audit_description", "")}',
                level=audit_message_tbi.get('audit_level', '')
            )
