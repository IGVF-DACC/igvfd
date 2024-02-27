from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('HumanDonor', frame='object')
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
    if 'related_donors' in value:
        for unique_related_donor in set([related_donor['donor'] for related_donor in value['related_donors']]):
            if [related_donor['donor'] for related_donor in value['related_donors']].count(unique_related_donor) > 1:
                detail = (
                    f'HumanDonor {audit_link(path_to_text(value["@id"]), value["@id"])} '
                    f'has a duplicated related donor {audit_link(path_to_text(unique_related_donor), unique_related_donor)}.'
                )
                yield AuditFailure('inconsistent related donors', detail, level='WARNING')
            related_donor_object = system.get('request').embed(unique_related_donor, '@@object?skip_calculated=true')
            if 'related_donors' not in related_donor_object or value['@id'] not in [related_donor['donor'] for related_donor in related_donor_object['related_donors']]:
                detail = (
                    f'HumanDonor {audit_link(path_to_text(value["@id"]), value["@id"])} '
                    f'has {audit_link(path_to_text(unique_related_donor), unique_related_donor)} '
                    f'as a related donor, but {audit_link(path_to_text(unique_related_donor), unique_related_donor)} '
                    f'does not mutually specify {audit_link(path_to_text(value["@id"]), value["@id"])} as a related donor.'
                )
                yield AuditFailure('inconsistent related donors', detail, level='ERROR')
