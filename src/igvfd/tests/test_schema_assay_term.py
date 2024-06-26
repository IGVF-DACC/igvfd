import pytest


def test_assay_term_term_id_regex(assay_term_starr, testapp):
    res = testapp.patch_json(
        assay_term_starr['@id'],
        {'term_id': 'ABC:12345'},
        expect_errors=True)
    assert res.status_code == 422


def test_assay_term_slims(
    assay_term_chip,
    assay_term_dnase,
    testapp
):
    res = testapp.get(assay_term_chip['@id'] + '@@index-data')
    expected_assay_slims = ['DNA binding']
    assert (all(slim in res.json['embedded']['assay_slims'] for slim in expected_assay_slims))

    res = testapp.get(assay_term_dnase['@id'] + '@@index-data')
    expected_category_slims = ['protein and DNA interaction']
    expected_objective_slims = ['protein and DNA interaction identification objective']
    assert (all(slim in res.json['embedded']['category_slims'] for slim in expected_category_slims))
    assert (all(slim in res.json['embedded']['objective_slims'] for slim in expected_objective_slims))
