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
    if ('nih_institutional_certification' not in value) and (any(donor.startswith('/human-donors/') for donor in value.get('donors'))):
        sample_id = value.get('@id')
        detail = (
            f'Biosample {audit_link(path_to_text(sample_id), sample_id)} '
            f'is missing NIH institutional certificate that is required for human samples.'
        )
        yield AuditFailure('missing nih_institutional_certification', detail, level='ERROR')


@audit_checker('Biosample', frame='object')
def audit_biosample_taxa_check(value, system):
    '''Flag biosamples associated with donors of different taxas.'''

    if 'donors' in value:
        sample_id = value['@id']
        donor_ids = value.get('donors')
        taxa_dict = {}
        for d in donor_ids:
            donor_object = system.get('request').embed(d + '@@object?skip_calculated=true')
            if donor_object.get('taxa'):
                taxa = donor_object.get('taxa')
                if taxa not in taxa_dict:
                    taxa_dict[taxa] = []

                taxa_dict[taxa].append(d)

        if len(taxa_dict) > 1:
            detail = ''
            for k, v in taxa_dict.items():
                detail += f'Biosample {audit_link(sample_id, sample_id)} has donors {audit_link(v, v)} that are {k}. '
            yield AuditFailure('inconsistent donor taxa', detail, level='ERROR')


BiosampleBase = (Tissue, WholeOrganism, PrimaryCell)


@audit_checker('BiosampleBase', frame='object')
def audit_age_properties(value, system):
    '''Tissue, WholeOrganism, PrimaryCell objects must specify a lower_bound_age, upper_bound_age and age_units.'''
    if 'lower_bound_age' and 'upper_bound_age' and 'age_units' not in value:
        value_id = system.get('path')
        detail = (
            f'Tissue {audit_link(path_to_text(value_id), value_id)} '
            f'is missing upper_bound_age, lower_bound_age, and age_units.'
        )
        yield AuditFailure('missing age properties', detail, level='WARNING')
