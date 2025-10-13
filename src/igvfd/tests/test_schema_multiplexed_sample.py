import pytest


def test_multiplexed_sample_protocols_regex(multiplexed_sample, testapp):
    res = testapp.patch_json(
        multiplexed_sample['@id'],
        {'protocols': ['https://www.protocols.io/123/ABC']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        multiplexed_sample['@id'],
        {'protocols': ['https://www.protocols.io/123/ABC', 'https://www.protocols.io/private/123/ABC']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        multiplexed_sample['@id'],
        {'protocols': ['https://www.protocols.io/private/123/ABC']})
    assert res.status_code == 200
    res = testapp.patch_json(
        multiplexed_sample['@id'],
        {'protocols': ['https://www.protocols.io/view/123/ABC']})
    assert res.status_code == 200
