from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('SequenceFile', frame='object')
def audit_sequence_file_no_seqspec(value, system):
    '''
        audit_detail: Linked seqspec configuration files are expected to have a seqspec content type.
        audit_category: inconsistent seqspec metadata
        audit_levels: ERROR
    '''
    if 'seqspec' in value:
        configuration_file_object = system.get('request').embed(value['seqspec'], '@@object?skip_calculated=true')
        if configuration_file_object.get('content_type') != 'seqspec':
            detail = (
                f'Sequence file {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'links to a seqspec file that does not have content_type "seqspec."'
            )
            yield AuditFailure('inconsistent seqspec metadata', detail, level='ERROR')
