from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('AnalysisSet', frame='object')
def audit_input_file_sets(value, system):
    '''
    [
        {
            "audit_description": "Primary analysis sets are expected to have at least one measurement set as an input file set.",
            "audit_category": "missing measurement set",
            "audit_level": "ERROR"
        }
    ]
    '''
    detail = ''
    if value.get('file_set_type') == 'primary analysis':
        if not(any(file_set.startswith('/measurement-sets/') for file_set in value['input_file_sets'])):
            detail = (
                f'AnalysisSet {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'is a primary analysis, but does not specify any measurement sets as '
                f'input_file_sets.'
            )
            yield AuditFailure('missing measurement set', detail, level='ERROR')
