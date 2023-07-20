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
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
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
    # Treatments in cell_fate_change_treatments should not be of purpose "perturbation", "agonist", "antagonist", or "control".
    testapp.patch_json(
        treatment_chemical['@id'],
        {
            'purpose': 'perturbation'
        }
    )
    testapp.patch_json(
        treatment_protein['@id'],
        {
            'purpose': 'control'
        }
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'cell_fate_change_treatments': [treatment_chemical['@id'], treatment_protein['@id']],
            'time_post_change': 5,
            'time_post_change_units': 'minute'
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent cell_fate_change_treatments treatment purpose'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        treatment_chemical['@id'],
        {
            'purpose': 'differentiation'
        }
    )
    testapp.patch_json(
        treatment_protein['@id'],
        {
            'purpose': 'de-differentiation'
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent cell_fate_change_treatments treatment purpose'
        for error in res.json['audit'].get('ERROR', [])
    )
