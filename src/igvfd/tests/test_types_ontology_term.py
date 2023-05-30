import pytest


def test_term_unique_keys(
    assay_term_starr,
    assay_term_chip,
    phenotype_term_alzheimers,
    phenotype_term_myocardial_infarction,
    sample_term_K562,
    sample_term_adrenal_gland,
    testapp
):
    res = testapp.patch_json(
        assay_term_starr['@id'],
        {'term_id': 'OBI:0000716'},
        expect_errors=True)
    assert res.status_code == 409
    res = testapp.patch_json(
        phenotype_term_alzheimers['@id'],
        {'term_id': 'HP:0001658'},
        expect_errors=True)
    assert res.status_code == 409
    res = testapp.patch_json(
        sample_term_K562['@id'],
        {'term_id': 'UBERON:0002369'},
        expect_errors=True)
    assert res.status_code == 409
    res = testapp.patch_json(
        sample_term_K562['@id'],
        {'term_id': 'UBERON:0002370'},
        expect_errors=False)
    assert res.status_code == 200


def test_term_ancestors(
    sample_term_K562,
    testapp
):
    res = testapp.get(sample_term_K562['@id'])
    assert 'ancestors' in res.json
    assert len(res.json.get('ancestors')) > 1


def test_ontology(
    sample_term_K562,
    testapp
):
    res = testapp.get(sample_term_K562['@id'])
    assert 'ontology' in res.json
    assert res.json.get('ontology') == 'EFO'
