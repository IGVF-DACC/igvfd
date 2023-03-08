import pytest


def test_measurement_set_moi_construct_library(
    testapp,
    measurement_set,
    construct_library_genome_wide
):
    res = testapp.patch_json(
        measurement_set['@id'],
        {'moi': 2.1},
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        measurement_set['@id'],
        {
            'moi': 2.1,
            'construct_libraries': [construct_library_genome_wide['@id']]
        }
    )
    assert res.status_code == 200


def test_patch_curated_set(award, lab, curated_set_genome, testapp):
    res = testapp.patch_json(
        curated_set_genome['@id'],
        {'curated_set_type': 'genome'})
    assert res.status_code == 200
    res = testapp.patch_json(
        curated_set_genome['@id'],
        {'taxa': 'Homo sapiens'})
    assert res.status_code == 200
