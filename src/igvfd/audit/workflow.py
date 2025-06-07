from snovault.auditor import (
    AuditFailure
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)
from .audit_registry import register_audit, register_all_audits


@register_audit(['Workflow'], frame='object')
def audit_workflow_without_asvs(value, system):
    '''
    [
        {
            "audit_description": "Workflows are expected to be associated with one or more analysis step version(s).",
            "audit_category": "missing analysis step versions",
            "audit_level": "WARNING"
        }
    ]
    '''
    # Audit 1: missing analysis step versions
    missing_asv_msg = get_audit_message(audit_workflow_without_asvs, index=0)
    if 'analysis_step_versions' not in value:
        detail = f'Workflow {audit_link(path_to_text(value["@id"]), value["@id"])} does not have any analysis step version.'
        yield AuditFailure(missing_asv_msg.get('audit_category', ''), f'{detail} {missing_asv_msg.get("audit_description", "")}', level=missing_asv_msg.get('audit_level', ''))


register_all_audits()
