import pytest


def test_audit_targeted_sample_term(
    testapp,
    in_vitro_cell_line,
    sample_term_K562
):
    # In vitro systems should not have the same sample_term specified in targeted_sample_term and biosample_term.
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'targeted_sample_term': sample_term_K562['@id']}
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@index-data')
    assert any(
        error['category'] == 'inconsistent targeted_sample_term'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_targeted_sample_term(
    testapp,
    in_vitro_cell_line,
    treatment_chemical,
    treatment_protein
):
    # Treatments in introduced_factors should not be of purpose "perturbation", "agonist", "antagonist", or "control".
    testapp.patch_json(
        treatment_chemical['@id'],
        {
            'purpose': 'perturbation'
        }
    )
    testapp.patch_json(
        treatment_chemical['@id'],
        {
            'purpose': 'control'
        }
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'introduced_factors': [treatment_chemical['@id'], treatment_protein['@id']],
            'time_post_factors_introduction': 5,
            'time_post_factors_introduction_units': 'minute'
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@index-data')
    print(res.json['audit'])
    assert any(
        error['category'] == 'inconsistent introduced_factors treatment purpose'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        treatment_chemical['@id'],
        {
            'purpose': 'differentiation'
        }
    )
    testapp.patch_json(
        treatment_chemical['@id'],
        {
            'purpose': 'de-differentiation'
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@index-data')
    assert all(
        error['category'] != 'inconsistent introduced_factors treatment purpose'
        for error in res.json['audit'].get('ERROR', [])
    )
