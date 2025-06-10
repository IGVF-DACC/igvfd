from snovault.auditor import (
    AuditFailure,
    audit_checker
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message,
    space_in_words
)
from .audit_registry import register_audit, run_audits


@register_audit(['File'], frame='object')
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
    if upload_status not in ['validated', 'validation exempted'] and not (value.get('externally_hosted', False)):
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


@register_audit(['File'], frame='object')
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


@register_audit(['MatrixFile', 'ModelFile', 'TabularFile'], frame='object')
def audit_file_no_file_format_specifications(value, system):
    '''
    [
        {
            "audit_description": "Tabular files, with the exception of vcf files, are expected to link to a file format specifications document describing the headers of the file.",
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
        if value.get('file_format') == 'vcf':
            return
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


@audit_checker('File', frame='object')
def audit_file_object_dispatcher(value, system):
    yield from run_audits(value, system, frame='object')


@audit_checker('MatrixFile', frame='object')
def audit_file_matrix_file_object_dispatcher(value, system):
    yield from run_audits(value, system, frame='object')


@audit_checker('ModelFile', frame='object')
def audit_file_model_file_object_dispatcher(value, system):
    yield from run_audits(value, system, frame='object')


@audit_checker('TabularFile', frame='object')
def audit_file_tabular_file_object_dispatcher(value, system):
    yield from run_audits(value, system, frame='object')
