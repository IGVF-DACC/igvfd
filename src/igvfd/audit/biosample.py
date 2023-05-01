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
        sample_id = value.get('@id')
        detail = (
            f'Biosample {audit_link(path_to_text(sample_id), sample_id)} '
            f'is missing NIH institutional certificate that is required for human samples.'
        )
        yield AuditFailure('missing nih_institutional_certification', detail, level='ERROR')
