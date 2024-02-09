from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


def check_for_seq_config_files(value):
    non_sequence_files = []
    for file in value.get('files'):
        if not(file.startswith('/sequence-files/') or file.startswith('/configuration-files/')):
            non_sequence_files.append(file)


@audit_checker('FileSet', frame='object')
def audit_no_files(value, system):
    '''
        audit_detail: File sets are expected to have files.
        audit_category: missing files
        audit_levels: WARNING
    '''
    if not(value.get('files', '')):
        detail = (
            f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no files.'
        )
        yield AuditFailure('missing files', detail, level='WARNING')
