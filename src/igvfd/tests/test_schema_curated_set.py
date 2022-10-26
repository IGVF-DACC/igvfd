import pytest


def test_post_curated_set(award, lab, testapp):
    res = testapp.post_json(
        '/curated_set',
        {
            'lab': lab['@id'],
            'award': award['@id']
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/curated_set',
        {
            'lab': lab['@id'],
            'award': award['@id'],
            'reference_type': 'transcriptome'
        })
    assert res.status_code == 201
