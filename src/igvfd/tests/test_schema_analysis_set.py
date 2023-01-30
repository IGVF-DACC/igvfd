import pytest


def test_analysis_set_sample_donor_dependency(
    testapp,
    analysis_set_with_donor,
    analysis_set_with_sample,
    human_donor,
    cell_line
):
    res = testapp.patch_json(
        analysis_set_with_donor['@id'],
        {'samples': [cell_line['@id']]},
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        analysis_set_with_sample['@id'],
        {'donors': [human_donor['@id']]},
        expect_errors=True
    )
    assert res.status_code == 422
