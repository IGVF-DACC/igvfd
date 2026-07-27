import pytest


def test_measurement_set_protocols_regex(measurement_set, testapp):
    res = testapp.patch_json(
        measurement_set['@id'],
        {'protocols': ['https://www.protocols.io/123/ABC']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        measurement_set['@id'],
        {'protocols': ['https://www.protocols.io/123/ABC', 'https://www.protocols.io/private/123/ABC']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        measurement_set['@id'],
        {'protocols': ['https://www.protocols.io/private/123/ABC']})
    assert res.status_code == 200
    res = testapp.patch_json(
        measurement_set['@id'],
        {'protocols': ['https://www.protocols.io/view/123/ABC']})
    assert res.status_code == 200


def test_measurement_set_dbxrefs_regex(measurement_set, testapp):
    res = testapp.patch_json(
        measurement_set['@id'],
        {'dbxrefs': ['not_a_valid_dbxref']},
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        measurement_set['@id'],
        {'dbxrefs': ['ENCODE:ENCFF000AAA']},
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        measurement_set['@id'],
        {'dbxrefs': ['GEO:GSE187549', 'urn:mavedb:00001250-a-1', 'ENCODE:ENCSR000AAA']}
    )
    assert res.status_code == 200
