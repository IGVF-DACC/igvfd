import pytest


def test_accession(human_donor, testapp):
    res = testapp.get(human_donor['@id'])
    assert res.json['accession'][:6] == 'IGVFDO'


def test_ethnicities(human_donor, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'ethnicities': ['European']})
    assert res.status_code == 200
    res = testapp.patch_json(
        human_donor['@id'],
        {'ethnicities': ['Elf']}, expect_errors=True)
    assert res.status_code == 422


def test_fail_donor_with_three_parents(human_donor, parent_human_donor_1, parent_human_donor_2, parent_human_donor_3, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'parents': [
            parent_human_donor_1['@id'],
            parent_human_donor_2['@id'],
            parent_human_donor_3['@id']
        ]}, expect_errors=True)
    assert res.status_code == 422


def test_fail_human_donor_with_rodent_parent(human_donor, parent_rodent_donor_1, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'parents': [
            parent_rodent_donor_1['@id']
        ]}, expect_errors=True)
    assert res.status_code == 422


def test_fail_human_donor_with_human_and_rodent_parents(human_donor, parent_human_donor_1, parent_rodent_donor_1, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'parents': [
            parent_human_donor_1['@id'],
            parent_rodent_donor_1['@id']
        ]}, expect_errors=True)
    assert res.status_code == 422


def test_collections(human_donor, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'collections': ['ENCODE']})
    assert res.status_code == 200


def test_collections_fail(human_donor, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'collections': ['Something not collection']}, expect_errors=True)
    assert res.status_code == 422


def test_taxa(award, lab, testapp):
    res = testapp.post_json(
        '/human_donor',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'taxa': 'Homo sapiens'
        })
    assert res.status_code == 201
    res = testapp.post_json(
        '/human_donor',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'taxa': 'Mus musculus'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/human_donor',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'taxa': 'Saccharomyces'
        }, expect_errors=True)
    assert res.status_code == 422


def test_human_traits(human_donor, phenotype_term_myocardial_infarction, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'traits':
            ['Myocardial infraction']
         }, expect_errors=True)
    assert res.status_code == 422  # confirming strings not allowed
    res = testapp.patch_json(
        human_donor['@id'],
        {'traits':
            [phenotype_term_myocardial_infarction['@id']]
         })
    assert res.status_code == 200  # confirming existing phenotype term allowed


def test_patch_parents(human_donor, parent_human_donor_1, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'parents': [
            parent_human_donor_1['@id']
        ]})
    assert res.status_code == 200


def test_patch_phenotypic_feature(human_donor, phenotypic_feature_basic, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'phenotypic_features': [
            phenotypic_feature_basic['@id']
        ]})
    assert res.status_code == 200
