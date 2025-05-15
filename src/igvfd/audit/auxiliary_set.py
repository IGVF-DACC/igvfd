from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message,
    register_audit,
    register_all_audits
)


@register_audit(['AuxiliarySet'], frame='object')
def audit_missing_measurement_sets(value, system):
    '''
    [
        {
            "audit_description": "Auxiliary sets are expected to be associated with a measurement set(s).",
            "audit_category": "missing measurement set",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message = get_audit_message(audit_missing_measurement_sets)
    measurement_sets = value.get('measurement_sets', [])
    if not (measurement_sets):
        detail = (
            f'Auxiliary set {audit_link(path_to_text(value["@id"]), value["@id"])} is not '
            f'associated with any `measurement_sets`.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


register_all_audits()
