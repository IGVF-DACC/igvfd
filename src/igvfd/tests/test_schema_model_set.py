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


def test_model_set_version_regex(
    testapp,
    model_set_no_input
):
    res = testapp.patch_json(
        model_set_no_input['@id'],
        {'model_version': 'v1111.22222.3333'}
    )
    assert res.status_code == 200
    res = testapp.patch_json(
        model_set_no_input['@id'],
        {'model_version': 'v1.0.0'}
    )
    assert res.status_code == 200
    res = testapp.patch_json(
        model_set_no_input['@id'],
        {'model_version': 'v0.0.0'},
        expect_errors=True
    )
    assert res.status_code == 422
