import pytest


def test_accession(rodent_donor, testapp):
    res = testapp.get(rodent_donor['@id'])
    assert res.json['accession'][:6] == 'IGVFDO'


def test_lot_id_dependency_success(rodent_donor, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'lot_id': 'R00002', 'product_id': 'UberMouse5000'})
    assert res.status_code == 200


def test_lot_id_dependency_fail(rodent_donor, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert res.status_code == 422


def test_strain(rodent_donor, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {
            'strain_background': 'C57BL/6J (B6)',
            'strain': 'B6.129P2-Tcrbtm1Mom/J',
            'genotype': 'Some Genotype'
        })
    assert res.status_code == 200


def test_fail_donor_with_three_parents(rodent_donor, parent_rodent_donor_1, parent_rodent_donor_2, parent_rodent_donor_3, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'parents': [
            parent_rodent_donor_1['@id'],
            parent_rodent_donor_2['@id'],
            parent_rodent_donor_3['@id']
        ]}, expect_errors=True)
    assert res.status_code == 422


def test_fail_rodent_donor_with_human_parents(rodent_donor, parent_human_donor_1, parent_human_donor_2, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'parents': [
            parent_human_donor_1['@id'],
            parent_human_donor_2['@id']
        ]}, expect_errors=True)
    assert res.status_code == 422


def test_fail_rodent_donor_with_rodent_and_human_parents(rodent_donor, parent_rodent_donor_1, parent_human_donor_2, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'parents': [
            parent_rodent_donor_1['@id'],
            parent_human_donor_2['@id']
        ]}, expect_errors=True)
    assert res.status_code == 422


def test_collections(rodent_donor, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'collections': [
            'ENCODE'
        ]})
    assert res.status_code == 200


def test_collections_fail(rodent_donor, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'collections': [
            'I am the very model of a modern major-general.'
        ]}, expect_errors=True)
    assert res.status_code == 422


def test_taxa(award, lab, testapp):
    res = testapp.post_json(
        '/rodent_donor',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'taxa': 'Mus musculus',
            'sex': 'male',
            'strain': 'B6'
        })
    assert res.status_code == 201
    res = testapp.post_json(
        '/rodent_donor',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'taxa': 'Homo sapiens',
            'sex': 'male',
            'strain': 'B6'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/rodent_donor',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'taxa': 'Saccharomyces',
            'sex': 'male',
            'strain': 'B6'
        }, expect_errors=True)
    assert res.status_code == 422


def test_rodent_traits(rodent_donor, phenotype_term_myocardial_infarction, phenotype_term_alzheimers, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'traits':
            ['HP:0001658', 'DOID:10652']
         }, expect_errors=True)
    assert res.status_code == 422  # confirming term_id strings not allowed
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'traits':
            [phenotype_term_myocardial_infarction['@id'], phenotype_term_alzheimers['@id']]
         })
    assert res.status_code == 200  # confirming existing phenotype terms allowed


def test_patch_parents(rodent_donor, parent_rodent_donor_1, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'parents': [
            parent_rodent_donor_1['@id']
        ]})
    assert res.status_code == 200


def test_patch_phenotypic_feature(rodent_donor, phenotypic_feature_basic, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'phenotypic_features': [
            phenotypic_feature_basic['@id']
        ]})
    assert res.status_code == 200


def test_rodent_identifier_dependency(rodent_donor, award, lab, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'individual_rodent': True}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'individual_rodent': True, 'rodent_identifier': '045'})
    assert res.status_code == 200
    res = testapp.delete(
        rodent_donor['@id'],
        {'individual_rodent'})
    assert res.status_code == 422
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'individual_rodent': False}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/rodent_donor',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'taxa': 'Mus musculus',
            'sex': 'male',
            'strain': 'PWK',
            'individual_rodent': False,
            'rodent_identifier': '123'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/rodent_donor',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'taxa': 'Mus musculus',
            'sex': 'male',
            'strain': 'PWK',
            'individual_rodent': False
        })
    assert res.status_code == 201
