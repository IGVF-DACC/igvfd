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
            "audit_description": "Files are expected to be validated or validation exempted.",
            "audit_category": "upload status not validated",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "External files are expected to be validated or validation exempted.",
            "audit_category": "upload status not validated",
            "audit_level": "WARNING"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    upload_status = value.get('upload_status')
    if upload_status not in ['validated', 'validation exempted']:
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


@audit_checker('MatrixFile', frame='object')
@audit_checker('ModelFile', frame='object')
@audit_checker('TabularFile', frame='object')
def audit_file_no_file_format_specifications(value, system):
    '''
    [
        {
            "audit_description": "Tabular files are expected to link to a file format specifications document describing the headers of the file.",
            "audit_category": "missing file format specifications",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Matrix files are expected to link to a file format specifications document describing the axes and layers of the file.",
            "audit_category": "missing file format specifications",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Model files in tsv format are expected to link to a file format specifications document describing the content of the file.",
            "audit_category": "missing file format specifications",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    if object_type == 'Tabular file':
        audit_message = get_audit_message(audit_file_no_file_format_specifications, index=0)
    elif object_type == 'Matrix file':
        audit_message = get_audit_message(audit_file_no_file_format_specifications, index=1)
    elif object_type == 'Model file':
        if value.get('file_format') != 'tsv':
            return
        audit_message = get_audit_message(audit_file_no_file_format_specifications, index=2)
    if not (value.get('file_format_specifications')):
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no `file_format_specifications`.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('SequenceFile', frame='object')
def audit_multiple_seqspec_per_seqfile(value, system):
    '''
    [
        {
            "audit_description": "A sequence file is expected to have only one released sequence specification file.",
            "audit_category": "multiple seqspecs per sequence file",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "A sequence file is expected to have only one in progress sequence specification file.",
            "audit_category": "multiple seqspecs per sequence file",
            "audit_level": "INTERNAL_ACTION"
        }
    ]
    '''
    audit_msg_multi_released_seqspec = get_audit_message(audit_function=audit_multiple_seqspec_per_seqfile, index=0)
    audit_msg_multi_inprogress_seqspec = get_audit_message(audit_function=audit_multiple_seqspec_per_seqfile, index=1)
    seqspec_files = value.get('seqspecs', '')
    if len(seqspec_files) > 1:
        all_seqspec_file_status = []
        for seqspec_file in seqspec_files:
            seqspec_file_obj = system.get('request').embed(seqspec_file, '@@object?skip_calculated=true')
            seqspec_file_status = seqspec_file_obj.get('status', '')
            all_seqspec_file_status.append(seqspec_file_status)
        if all_seqspec_file_status.count('released') > 1:
            detail = (
                f'Sequence File {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has multiple released sequence specification files.'
            )
            yield AuditFailure(audit_msg_multi_released_seqspec.get('audit_category', ''), f'{detail} {audit_msg_multi_released_seqspec.get("audit_description", "")}', level=audit_msg_multi_released_seqspec.get('audit_level', ''))
        elif all_seqspec_file_status.count('in progress') > 1:
            detail = (
                f'Sequence File {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has multiple in progress sequence specification files.'
            )
            yield AuditFailure(audit_msg_multi_inprogress_seqspec.get('audit_category', ''), f'{detail} {audit_msg_multi_inprogress_seqspec.get("audit_description", "")}', level=audit_msg_multi_inprogress_seqspec.get('audit_level', ''))
