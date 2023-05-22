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
