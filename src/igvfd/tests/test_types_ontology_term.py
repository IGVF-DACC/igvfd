import pytest


def test_ontology_term_unique_keys(
    assay_ontology_term_starr,
    assay_ontology_term_chip,
    phenotype_ontology_term_alzheimers,
    phenotype_ontology_term_myocardial_infarction,
    sample_ontology_term_K562,
    sample_ontology_term_adrenal_gland,
    testapp
):
    res = testapp.patch_json(
        assay_ontology_term_starr['@id'],
        {'term_id': 'OBI:0000716'},
        expect_errors=True)
    assert res.status_code == 409
    res = testapp.patch_json(
        phenotype_ontology_term_alzheimers['@id'],
        {'term_id': 'HP:0001658'},
        expect_errors=True)
    assert res.status_code == 409
    res = testapp.patch_json(
        sample_ontology_term_K562['@id'],
        {'term_id': 'UBERON:0002369'},
        expect_errors=True)
    assert res.status_code == 409
    res = testapp.patch_json(
        sample_ontology_term_K562['@id'],
        {'term_id': 'UBERON:0002370'},
        expect_errors=False)
    assert res.status_code == 200
