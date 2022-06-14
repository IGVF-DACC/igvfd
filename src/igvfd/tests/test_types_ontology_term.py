import pytest


def test_ontology_term_unique_keys(
    assay_ontology_term_starr,
    assay_ontology_term_chip,
    disease_ontology_term_alzheimers,
    disease_ontology_term_myocardial_infarction,
    sample_ontology_term_K562,
    sample_ontology_term_adrenal_gland,
    testapp
):
    res = testapp.patch_json(
        assay_ontology_term_starr['@id'],
        {'term_id': 'OBI:0000716'},
        expect_errors=True)
    print(res)
    assert res.status_code == 409
    res = testapp.patch_json(
        disease_ontology_term_alzheimers['@id'],
        {'term_id': 'HP:0001658'},
        expect_errors=True)
    assert res.status_code == 409
    res = testapp.patch_json(
        sample_ontology_term_K562['@id'],
        {'term_id': 'UBERON:0002369'},
        expect_errors=True)
    assert res.status_code == 409
