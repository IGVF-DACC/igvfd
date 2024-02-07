from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('AuxiliarySet', frame='object')
def audit_auxiliary_set_files(value, system):
    '''
        audit_detail: Auxiliary sets are not expected to have any files except sequence files or configuration files.
        audit_category: unexpected file association
        audit_levels: WARNING
    '''
    non_sequence_files = []
    for file in value.get('files'):
        if not(file.startswith('/sequence-files/') or file.startswith('/configuration-files/')):
            non_sequence_files.append(file)
    if non_sequence_files:
        non_sequence_files = ', '.join(
            [audit_link(path_to_text(file), file) for file in non_sequence_files])
        detail = (f'AuxiliarySet {audit_link(path_to_text(value["@id"]),value["@id"])} links to '
                  f'file(s) that are not sequence or configuration files: {non_sequence_files}. This is unexpected as '
                  f'auxiliary sets are only expected to host sequence files or configuration files.')
        yield AuditFailure('unexpected file association', detail, level='WARNING')