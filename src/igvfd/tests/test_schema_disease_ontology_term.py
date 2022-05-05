import pytest


def test_disease_ontology_term_term_id_regex(disease_ontology_term_alzheimers, testapp):
    res = testapp.patch_json(
        disease_ontology_term_alzheimers['@id'],
        {'term_id': 'ABC:12345'},
        expect_errors=True)
    assert(res.status_code == 422)
