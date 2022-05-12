import pytest


def test_trait_ontology_term_term_id_regex(trait_ontology_term_epilepsy, testapp):
    res = testapp.patch_json(
        trait_ontology_term_epilepsy['@id'],
        {'term_id': 'ABC:12345'},
        expect_errors=True)
    assert(res.status_code == 422)
