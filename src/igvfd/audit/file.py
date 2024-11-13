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


@audit_checker('AlignmentFile', frame='object')
def audit_bai_alignment_files(value, system):
    '''
    [
        {
            "audit_description": "Alignment files in bai format are expected to have their corresponding bam file in `derived_from`.",
            "audit_category": "incorrect bam file",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message = get_audit_message(audit_bai_alignment_files)
    object_type = space_in_words(value['@type'][0]).capitalize()
    check_properties_list = ['content_type', 'assembly', 'filtered', 'redacted', 'transcriptome_annotation']
    inconsistent_properties_list = []
    if value.get('file_format') == 'bai':
        if 'derived_from' not in value:
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has no bam file in `derived_from`.')
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))
        else:
            derived_from_file = value.get('derived_from')
            if len(derived_from_file) > 1:
                detail = (
                    f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has multiple files in `derived_from`.')
                yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))
            else:
                derived_from_file_obj = system.get('request').embed(
                    derived_from_file[0], '@@object?skip_calculated=true')
                if derived_from_file_obj.get('file_format') != 'bam':
                    detail = (
                        f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has incorrect file in `derived_from`.')
                    yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))
                else:
                    for property in check_properties_list:
                        if value.get(property) != derived_from_file_obj.get(property):
                            inconsistent_properties_list.append(property)
                    if inconsistent_properties_list:
                        inconsistent_properties_str = ', '.join(inconsistent_properties_list)
                        detail = (f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has the following inconsistent properties with its bam file in `derived_from`: '
                                  f'{inconsistent_properties_str}.')
                        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))
