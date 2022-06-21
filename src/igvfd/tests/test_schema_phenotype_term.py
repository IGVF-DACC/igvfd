import pytest


def test_phenotype_term_term_id_regex(phenotype_term_alzheimers, testapp):
    res = testapp.patch_json(
        phenotype_term_alzheimers['@id'],
        {'term_id': 'ABC:12345'},
        expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        phenotype_term_alzheimers['@id'],
        {'term_id': 'DOID:10652'},
        expect_errors=False)
    assert res.status_code == 200


def test_phenotype_term_required_term_name(phenotype_term_incomplete, testapp):
    res = testapp.post_json(
        '/phenotype_term',
        phenotype_term_incomplete,
        expect_errors=True)
    assert res.status_code == 422
