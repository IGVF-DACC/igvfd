from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message,
    space_in_words
)


@audit_checker('Biosample', frame='object')
def audit_biosample_taxa_check(value, system):
    '''
    [
        {
            "audit_description": "Biosamples are expected to have donors with the same taxa.",
            "audit_category": "inconsistent donor taxa",
            "audit_level": "ERROR"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_biosample_taxa_check)
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
            detail = f'{object_type} {audit_link(path_to_text(sample_id), sample_id)} has `donors` with `taxa` {taxa_detail}. '
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('Tissue', frame='object')
@audit_checker('PrimaryCell', frame='object')
@audit_checker('WholeOrganism', frame='object')
def audit_biosample_age(value, system):
    '''
    [
        {
            "audit_description": "Tissues, primary cells, and whole organisms are expected to specify a lower bound age, upper bound age, and age units.",
            "audit_category": "missing age",
            "audit_level": "WARNING"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_biosample_age)
    if 'lower_bound_age' not in value and 'upper_bound_age' not in value and 'age_units' not in value:
        value_id = system.get('path')
        detail = (
            f'{object_type} {audit_link(path_to_text(value_id), value_id)} '
            f'is missing `upper_bound_age`, `lower_bound_age`, and `age_units`.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('Biosample', frame='object')
def audit_biomarker_name(value, system):
    '''
    [
        {
            "audit_description": "Biosamples are expected to have biomarkers with different names.",
            "audit_category": "inconsistent biomarkers",
            "audit_level": "ERROR"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_biomarker_name)
    if 'biomarkers' in value:
        sample_id = value['@id']
        biomarker_ids = value.get('biomarkers')
        biomarker_dict = {}
        for b in biomarker_ids:
            biomarker_object = system.get('request').embed(b + '@@object?skip_calculated=true')
            name = biomarker_object.get('name')
            if name not in biomarker_dict:
                biomarker_dict[name] = []

            biomarker_dict[name].append(b)

        for name, b_ids in biomarker_dict.items():
            if len(b_ids) > 1:
                biomarkers_to_link = ', '.join([audit_link(path_to_text(b_id), b_id) for b_id in b_ids])
                detail = (
                    f'{object_type} {audit_link(path_to_text(sample_id), sample_id)} has conflicting biomarkers '
                    f'{biomarkers_to_link} with the same `name`: {name}.'
                )
                yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('Biosample', frame='object')
def audit_multiple_ics_with_mismatched_access(value, system):
    '''
    [
        {
            "audit_description": "If a biosample has more than one institutional certificate, it is expected for all of them to have the same controlled_access.",
            "audit_category": "inconsistent institutional certificates",
            "audit_level": "INTERNAL_ACTION"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_multiple_ics_with_mismatched_access)
    if 'institutional_certificates' in value:
        ic_controlled_access_values = dict()
        for ic in value['institutional_certificates']:
            ic_object = system.get('request').embed(ic + '@@object')
            if ic_object.get('controlled_access', '') not in ic_controlled_access_values:
                ic_controlled_access_values[ic_object.get('controlled_access', '')] = [(
                    ic_object.get('certificate_identifier', ''), ic_object.get('@id', ''))]
            else:
                ic_controlled_access_values[ic_object.get('controlled_access', '')].append(
                    (ic_object.get('certificate_identifier', ''), ic_object.get('@id', '')))

        if len(ic_controlled_access_values) > 1:
            controlled_links = ', '.join(
                [audit_link(x[0], x[1]) for x in ic_controlled_access_values[True]]
            )
            uncontrolled_links = ', '.join(
                [audit_link(x[0], x[1]) for x in ic_controlled_access_values[False]]
            )
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has both '
                f'controlled access institutional certificates {controlled_links} and '
                f'uncontrolled access institutional certificates {uncontrolled_links}.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))
