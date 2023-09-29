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


def test_nucleic_acid_delivery_enum(testapp, measurement_set):
    res = testapp.patch_json(
        measurement_set['@id'],
        {'nucleic_acid_delivery': 'adenoviral transduction'})
    assert res.status_code == 200
    res = testapp.patch_json(
        measurement_set['@id'],
        {'nucleic_acid_delivery': 'Something not in the enum list'}, expect_errors=True)
    assert res.status_code == 422
