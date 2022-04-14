import pytest


def test_sample_ontology_term_term_id_regex(sample_ontology_term_1, testapp):
    res = testapp.get(biosample_1['@id'])
    res = testapp.patch_json(
        sample_ontology_term_1['@id'],
        {'term_id': 'ABC:12345'})
    assert(res.status_code == 422)
