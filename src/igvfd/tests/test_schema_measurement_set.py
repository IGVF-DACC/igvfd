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


def test_seqspec_pattern(testapp, measurement_set):
    res = testapp.patch_json(
        measurement_set['@id'],
        {'seqspec': 'http://github.com/IGVF/seqspec/blob/main/assays/mcSCRB-seq/spec.yaml'}
    )
    assert res.status_code == 200
    res = testapp.patch_json(
        measurement_set['@id'],
        {'seqspec': 'https://githubxcom/IGVF/seqspec/blob/main/assays/mcSCRB-seq/specxyaml'},
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        measurement_set['@id'],
        {'seqspec': 'https://github.com/IGVF/seqspec/tree/main/assays/mcSCRB-seq/spec.yaml'},
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        measurement_set['@id'],
        {'seqspec': 'https://github.com/IGVF/seqspec/blob/main/assays/mcSCRB-seq/spec.txt'},
        expect_errors=True
    )
    assert res.status_code == 422
