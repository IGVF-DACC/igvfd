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
    '''HumanDonors should have unique related donors and should be mutually specified
    between each HumanDonor in their related donors.'''
    if 'related_donors' in value:
        for i in range(len(value['related_donors'])):
            for j in range(i + 1, len(value['related_donors'])):
                if value['related_donors'][i]['donor'] == value['related_donors'][j]['donor']:
                    duplicated_donor = value['related_donors'][i]['donor']
                    detail = (
                        f'HumanDonor {audit_link(path_to_text(value["@id"]), value["@id"])} '
                        f'has a duplicated related donor {audit_link(path_to_text(duplicated_donor), duplicated_donor)}.'
                    )
                    yield AuditFailure('inconsistent related donors metadata', detail, level='WARNING')
                related_donor_object = system.get('request').embed(
                    value['related_donors'][j]['donor'], '@@object?skip_calculated=true')
                if 'related_donors' not in related_donor_object or value['@id'] not in [donor for donor in related_donor_object['related_donors']['donor']]:
                    related_donor_not_mutual = value['related_donors'][j]['donor']
                    detail = (
                        f'HumanDonor {audit_link(path_to_text(value["@id"]), value["@id"])} '
                        f'has {audit_link(path_to_text(related_donor_not_mutual), related_donor_not_mutual)} '
                        f'as a related donor, but {audit_link(path_to_text(related_donor_not_mutual), related_donor_not_mutual)} '
                        f'does not mutually specify {audit_link(path_to_text(value["@id"]), value["@id"])} as a related donor.'
                    )
                    yield AuditFailure('inconsistent related donors metadata', detail, level='ERROR')
