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
    '''
        audit_detail: Biosamples should specify a NIH Institutional Certification required for human data.
        audit_category: missing nih_institutional_certification
        audit_levels: ERROR
    '''
    if ('nih_institutional_certification' not in value) and (any(donor.startswith('/human-donors/') for donor in value.get('donors'))):
        sample_id = value.get('@id')
        detail = (
            f'Biosample {audit_link(path_to_text(sample_id), sample_id)} '
            f'is missing NIH institutional certificate that is required for human samples.'
        )
        yield AuditFailure('missing nih_institutional_certification', detail, level='ERROR')


@audit_checker('Biosample', frame='object')
def audit_biosample_taxa_check(value, system):
    '''
        audit_detail: Biosamples are not expected to have donors with different taxa.
        audit_category: inconsistent donor taxa
        audit_levels: ERROR
    '''
    if 'donors' in value:
        sample_id = value['@id']
        donor_ids = value.get('donors')
        taxa_dict = {}
        for d in donor_ids:
            donor_object = system.get('request').embed(d + '@@object?skip_calculated=true')
            d_link = audit_link(path_to_text(d), d)
            if donor_object.get('taxa'):
                taxa = donor_object.get('taxa')
                if taxa not in taxa_dict:
                    taxa_dict[taxa] = []

                taxa_dict[taxa].append(d_link)

        if len(taxa_dict) > 1:
            taxa_donors = []
            for k, v in taxa_dict.items():
                taxa_donors.append(f'{k} ({", ".join(v)})')
            taxa_detail = ', '.join(taxa_donors)
            detail = f'Biosample {audit_link(path_to_text(sample_id), sample_id)} has donors of taxas {taxa_detail}. '
            yield AuditFailure('inconsistent donor taxa', detail, level='ERROR')


@audit_checker('Biosample', frame='object')
def audit_biosample_age(value, system):
    '''
        audit_detail: Tissues, primacy cells, and whole organisms should specify a lower_bound_age, upper_bound_age and age_units.
        audit_category: missing age properties
        audit_levels: WARNING
    '''
    if ('Tissue' in value['@type']) or ('PrimaryCell' in value['@type']) or ('WholeOrganism' in value['@type']):
        if 'lower_bound_age' and 'upper_bound_age' and 'age_units' not in value:
            value_id = system.get('path')
            detail = (
                f'Biosample {audit_link(path_to_text(value_id), value_id)} '
                f'is missing upper_bound_age, lower_bound_age, and age_units.'
            )
            yield AuditFailure('missing age properties', detail, level='WARNING')
