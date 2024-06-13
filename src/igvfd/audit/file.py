from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_description,
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
            description = get_audit_description(audit_upload_status, index=1)
        else:
            audit_level = 'ERROR'
            description = get_audit_description(audit_upload_status, index=0)
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has `upload_status` {upload_status}.'
        )
        validation_error_detail = value.get('validation_error_detail')
        if upload_status == 'invalidated' and validation_error_detail:
            detail = f'{detail} Validation error detail: {validation_error_detail}'
        yield AuditFailure(
            'upload status not validated',
            f'{detail} {description}',
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
    for document in value.get('file_format_specifications', []):
        document_object = system.get('request').embed(document)
        doc_type = document_object['document_type']
        if doc_type != 'file format specification':
            detail = ('File {} has document {} of type {}'.format(
                audit_link(path_to_text(value['@id']), value['@id']),
                audit_link(path_to_text(document), document),
                doc_type
            )
            )
            yield AuditFailure('inconsistent document type', detail, level='ERROR')
