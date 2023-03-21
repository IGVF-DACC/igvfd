import pytest


def test_technical_sample(technical_sample, testapp):
    res = testapp.get(technical_sample['@id'])
    assert res.json['accession'][:6] == 'IGVFSM'


def test_technical_sample_lot_id_dependency(technical_sample, testapp):
    res = testapp.patch_json(
        technical_sample['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert res.status_code == 422


def test_technical_sample_type_dependency(technical_sample, testapp):
    res = testapp.patch_json(
        technical_sample['@id'],
        {'sample_material': 'inorganic'})
    assert res.status_code == 200
    res = testapp.patch_json(
        technical_sample['@id'],
        {'sample_material': 'not a real type'}, expect_errors=True)
    assert res.status_code == 422


def test_collections(technical_sample, testapp):
    res = testapp.patch_json(
        technical_sample['@id'],
        {'collections': ['ENCODE']})
    assert res.status_code == 200
    res = testapp.patch_json(
        technical_sample['@id'],
        {'collections': ['ABBBCCCHD1455']}, expect_errors=True)
    assert res.status_code == 422


def test_technical_sample_archived(technical_sample, testapp):
    res = testapp.patch_json(
        technical_sample['@id'],
        {'status': 'archived'})
    assert res.status_code == 200


def test_technical_sample_technical_sample_term(
    award,
    other_lab,
    source,
    sample_term_technical_sample,
    testapp
):
    item_missing_term = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'source': source['@id'],
        'sample_material': 'synthetic'
    }
    res = testapp.post_json(
        '/technical_sample',
        item_missing_term,
        expect_errors=True)
    assert res.status_code == 422

    item_with_term = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'source': source['@id'],
        'sample_material': 'synthetic',
        'technical_sample_term': sample_term_technical_sample['@id']
    }
    res = testapp.post_json(
        '/technical_sample',
        item_with_term)
    assert res.status_code == 201


def test_sorted_fraction_detail_dependency(testapp, technical_sample, primary_cell):
    res = testapp.patch_json(
        technical_sample['@id'],
        {'sorted_fraction': primary_cell['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        technical_sample['@id'],
        {'sorted_fraction_detail': 'I am a sorted fraction detail.'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        technical_sample['@id'],
        {'sorted_fraction': primary_cell['@id'],
         'sorted_fraction_detail': 'I am a sorted fraction detail.'})
    assert res.status_code == 200
