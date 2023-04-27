from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('Biosample', frame='object')
def audit_biosample_nih_institutional_certification(value, system):
    '''Biosample objects must specify an NIH Institutional Certification required for human data.'''
    if ('nih_institutional_certification' not in value) and (value.get('taxa') == 'Homo sapiens'):
        value_id = system.get('path')
        detail = (
            f'Biosample {audit_link(path_to_text(value_id), value_id)} '
            f'is missing NIH institutional certification required for human data.'
        )
        yield AuditFailure('missing nih_institutional_certification', detail, level='ERROR')
