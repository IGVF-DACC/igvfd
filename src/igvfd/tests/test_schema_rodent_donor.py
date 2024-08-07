import pytest


def test_accession(rodent_donor, testapp):
    res = testapp.get(rodent_donor['@id'])
    assert res.json['accession'][:6] == 'IGVFDO'


def test_lot_id_dependency_success(rodent_donor, source, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'lot_id': 'R00002', 'product_id': 'UberMouse5000', 'sources': [source['@id']]})
    assert res.status_code == 200


def test_lot_id_dependency_fail(rodent_donor, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert res.status_code == 422


def test_product_id_dependency(rodent_donor, source, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'product_id': '1234'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'product_id': '1234', 'sources': [source['@id']]})
    assert res.status_code == 200


def test_strain(rodent_donor, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {
            'strain_background': 'C57BL/6J (B6)',
            'strain': 'B6.129P2-Tcrbtm1Mom/J',
            'genotype': 'Some Genotype'
        })
    assert res.status_code == 200


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
    rodent_donor_no_individual_rodent = testapp.get(rodent_donor['@id'] + '@@edit').json
    rodent_donor_no_individual_rodent.pop('individual_rodent')
    res = testapp.put_json(rodent_donor['@id'], rodent_donor_no_individual_rodent, expect_errors=True)
    assert res.status_code == 422
