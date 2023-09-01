import pytest


def test_model_set_sample_donor_dependency(
    testapp,
    model_set_no_input,
    human_donor,
    in_vitro_cell_line
):
    res = testapp.patch_json(
        model_set_no_input['@id'],
        {'samples': [in_vitro_cell_line['@id']]},
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        model_set_no_input['@id'],
        {'donors': [human_donor['@id']]},
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        model_set_no_input['@id'],
        {'samples': [in_vitro_cell_line['@id']],
         'donors': [human_donor['@id']]},
        expect_errors=True
    )
    assert res.status_code == 422
