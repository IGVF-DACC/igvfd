import pytest


def test_model_sample_donor_dependency(
    testapp,
    model_no_input,
    human_donor,
    in_vitro_cell_line
):
    res = testapp.patch_json(
        model_no_input['@id'],
        {'samples': [in_vitro_cell_line['@id']],
         'donors': [human_donor['@id']]},
        expect_errors=True
    )
    print(res.status_code)
    assert res.status_code == 422
