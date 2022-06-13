import pytest


def test_sample_ontology_term_term_id_regex(sample_ontology_term_1, testapp):
    res = testapp.patch_json(
        sample_ontology_term_1['@id'],
        {'term_id': 'ABC:12345'},
        expect_errors=True)
    assert res.status_code == 422


def test_sample_ontology_term_slims(sample_ontology_term_1, testapp):
    res = testapp.get(sample_ontology_term_1['@id'] + '@@index-data')
    expected_organ_slims = ['blood', 'bodily fluid']
    expected_cell_slims = ['hematopoietic cell', 'cancer cell', 'leukocyte']
    expected_developmental_slims = ['mesoderm']
    expected_system_slims = ['immune system']
    assert(all(slim in res.json['embedded']['organ_slims'] for slim in expected_organ_slims))
    assert(all(slim in res.json['embedded']['cell_slims'] for slim in expected_cell_slims))
    assert(all(slim in res.json['embedded']['developmental_slims'] for slim in expected_developmental_slims))
    assert(all(slim in res.json['embedded']['system_slims'] for slim in expected_system_slims))
