import pytest


def test_assay_ontology_term_term_id_regex(assay_ontology_term_1, testapp):
    res = testapp.patch_json(
        assay_ontology_term_1['@id'],
        {'term_id': 'ABC:12345'},
        expect_errors=True)
    assert(res.status_code == 422)


def test_assay_ontology_term_slims(assay_ontology_term_1, testapp):
    res = testapp.get(assay_ontology_term_1['@id'] + '@@index-data')
    expected_assay_slims = ['Massively parallel reporter assay']
    assert(all(slim in res.json['embedded']['assay_slims'] for slim in expected_assay_slims))
