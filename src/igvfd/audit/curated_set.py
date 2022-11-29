from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('CuratedSet', frame='object')
def audit_curated_set_docs(value, system):
    detail = 'AUDIT!'
    yield AuditFailure('inconsistent standards document',
                       detail, level='WARNING')
