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
        audit_detail: Sequence files are expected to link to the associated seqspec YAML configuration file.
        audit_category: inconsistent seqspec metadata
        audit_levels: WARNING, ERROR
    '''
    if 'seqspec' not in value:
        detail = (
            f'Sequence file {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'is missing a link to its associated YAML configuration file.'
        )
        yield AuditFailure('inconsistent seqspec metadata', detail, level='WARNING')
    else:
        configuration_file_object = system.get('request').embed(value['seqspec'], '@@object?skip_calculated=true')
        if configuration_file_object.get('content_type') != 'seqspec':
            detail = (
                f'Sequence file {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'links to a seqspec file that does not have content_type "seqspec."'
            )
            yield AuditFailure('inconsistent seqspec metadata', detail, level='ERROR')
