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
            'file_set_type': 'transcriptome'
        })
    assert res.status_code == 201


def test_patch_curated_set(award, lab, curated_set_genome, testapp):
    res = testapp.patch_json(
        curated_set_genome['@id'],
        {'file_set_type': 'genome'})
    assert res.status_code == 200
    res = testapp.patch_json(
        curated_set_genome['@id'],
        {'taxa': 'Homo sapiens'})
    assert res.status_code == 200


def test_curated_set_assay_term(award, lab, curated_set_genome, assay_term_starr, testapp):
    res = testapp.patch_json(
        curated_set_genome['@id'],
        {'preferred_assay_titles': ['SHARE-seq']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        curated_set_genome['@id'],
        {'assay_term': assay_term_starr['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        curated_set_genome['@id'],
        {
            'preferred_assay_titles': ['SHARE-seq'],
            'assay_term': assay_term_starr['@id'],
            'file_set_type': 'external sequencing data'
        }
    )
    assert res.status_code == 200
