import pytest


def test_sample_ontology_term_term_id_regex(sample_ontology_term_1, testapp):
    res = testapp.patch_json(
        sample_ontology_term_1['@id'],
        {'term_id': 'ABC:12345'},
        expect_errors=True)
    assert(res.status_code == 422)
