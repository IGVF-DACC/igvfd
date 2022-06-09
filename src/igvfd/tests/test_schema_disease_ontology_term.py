import pytest


def test_disease_ontology_term_term_id_regex(disease_ontology_term_alzheimers, testapp):
    res = testapp.patch_json(
        disease_ontology_term_alzheimers['@id'],
        {'term_id': 'ABC:12345'},
        expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        disease_ontology_term_alzheimers['@id'],
        {'term_id': 'DOID:10652'},
        expect_errors=False)
    assert res.status_code == 200


def test_disease_ontology_term_required_term_name(disease_ontology_term_incomplete, testapp):
    res = testapp.post_json(
        '/disease_ontology_term',
        disease_ontology_term_incomplete,
        expect_errors=True)
    assert res.status_code == 422
