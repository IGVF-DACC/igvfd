import pytest


def test_summary(testapp, tissue, human_donor, rodent_donor, parent_rodent_donor_2, sample_term_brown_adipose_tissue, phenotype_term_alzheimers, treatment_chemical):
    res = testapp.get(tissue['@id'])
    assert res.json.get('summary') == 'adrenal gland tissue, male, Mus musculus strain1'
    testapp.patch_json(
        tissue['@id'],
        {
            'lower_bound_age': 10,
            'upper_bound_age': 10,
            'age_units': 'month'
        }
    )
    res = testapp.get(tissue['@id'])
    assert res.json.get('summary') == 'adrenal gland tissue, male, Mus musculus strain1 (10 months)'
    testapp.patch_json(
        human_donor['@id'],
        {
            'sex': 'male',
        }
    )
    testapp.patch_json(
        tissue['@id'],
        {
            'lower_bound_age': 50,
            'upper_bound_age': 100,
            'age_units': 'day',
            'virtual': True,
            'embryonic': True,
            'donors': [human_donor['@id']],
            'sample_terms': [sample_term_brown_adipose_tissue['@id']],
        }
    )
    res = testapp.get(tissue['@id'])
    assert res.json.get('summary') == 'virtual embryonic brown adipose tissue, male, Homo sapiens (50-100 days)'
    testapp.patch_json(
        rodent_donor['@id'],
        {
            'sex': 'female',
        }
    )
    testapp.patch_json(
        parent_rodent_donor_2['@id'],
        {
            'sex': 'male',
        }
    )
    testapp.patch_json(
        tissue['@id'],
        {
            'donors': [rodent_donor['@id'], parent_rodent_donor_2['@id']],
            'treatments': [treatment_chemical['@id']],
            'disease_terms': [phenotype_term_alzheimers['@id']],
            'cellular_sub_pool': 'PKR-1128',
        }
    )
    res = testapp.get(tissue['@id'])
    assert res.json.get(
        'summary') == f'virtual embryonic brown adipose tissue (cellular sub pool: PKR-1128), mixed sex, Mus musculus strain1, strain3 (50-100 days) associated with Alzheimer\'s disease, treated with 10 mM lactate for 1 hour'
