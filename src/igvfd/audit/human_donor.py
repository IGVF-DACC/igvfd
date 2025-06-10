from snovault.auditor import (
    AuditFailure,
    audit_checker
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)
from .audit_registry import register_audit, run_audits


@register_audit(['HumanDonor'], frame='object')
def audit_related_donors(value, system):
    '''
    [
        {
            "audit_description": "The human donors indicated in the list of related donors are expected to be unique.",
            "audit_category": "inconsistent related donors",
            "audit_level": "WARNING"
        },
        {
            "audit_description": "The human donors indicated in the list of related donors are expected to include a mutual link to the corresponding donor.",
            "audit_category": "inconsistent related donors",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message_unique = get_audit_message(audit_related_donors)
    audit_message_mutual = get_audit_message(audit_related_donors, index=1)
    if 'related_donors' in value:
        for unique_related_donor in set([related_donor['donor'] for related_donor in value['related_donors']]):
            if [related_donor['donor'] for related_donor in value['related_donors']].count(unique_related_donor) > 1:
                detail = (
                    f'Human donor {audit_link(path_to_text(value["@id"]), value["@id"])} '
                    f'has a duplicated related donor {audit_link(path_to_text(unique_related_donor), unique_related_donor)} in `related_donors`.'
                )
                yield AuditFailure(audit_message_unique.get('audit_category', ''), f'{detail} {audit_message_unique.get("audit_description", "")}', level=audit_message_unique.get('audit_level', ''))
            related_donor_object = system.get('request').embed(unique_related_donor, '@@object?skip_calculated=true')
            if 'related_donors' not in related_donor_object or value['@id'] not in [related_donor['donor'] for related_donor in related_donor_object['related_donors']]:
                detail = (
                    f'Human donor {audit_link(path_to_text(value["@id"]), value["@id"])} '
                    f'has {audit_link(path_to_text(unique_related_donor), unique_related_donor)} '
                    f'as a related donor, but {audit_link(path_to_text(unique_related_donor), unique_related_donor)} '
                    f'does not mutually specify {audit_link(path_to_text(value["@id"]), value["@id"])} as a related donor in `related_donors`.'
                )
                yield AuditFailure(audit_message_mutual.get('audit_category', ''), f'{detail} {audit_message_mutual.get("audit_description", "")}', level=audit_message_mutual.get('audit_level', ''))


@audit_checker('HumanDonor', frame='object')
def audit_human_donor_object_dispatcher(value, system):
    yield from run_audits(value, system, frame='object')
