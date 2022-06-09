import pytest


def test_assay_ontology_term_term_id_regex(assay_ontology_term_starr, testapp):
    res = testapp.patch_json(
        assay_ontology_term_starr['@id'],
        {'term_id': 'ABC:12345'},
        expect_errors=True)
    assert res.status_code == 422


def test_assay_ontology_term_slims(assay_ontology_term_chip, testapp):
    res = testapp.get(assay_ontology_term_chip['@id'] + '@@index-data')
    expected_assay_slims = ['DNA binding']
    assert(all(slim in res.json['embedded']['category_slims'] for slim in expected_assay_slims))
