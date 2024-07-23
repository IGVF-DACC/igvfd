import pytest


def test_accession(whole_organism, testapp):
    res = testapp.get(whole_organism['@id'])
    assert res.json['accession'][:6] == 'IGVFSM'


def test_lot_id_dependency(whole_organism, testapp):
    res = testapp.patch_json(
        whole_organism['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert res.status_code == 422


def test_product_id_dependency(award, lab, source, rodent_donor, sample_term_whole_organism, testapp):
    res = testapp.post_json(
        '/whole_organism',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'product_id': '700',
            'donors': [rodent_donor['@id']],
            'sample_terms': [sample_term_whole_organism['@id']]
        },
        expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/whole_organism',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'sources': [source['@id']],
            'product_id': '700',
            'donors': [rodent_donor['@id']],
            'sample_terms': [sample_term_whole_organism['@id']]
        })
    assert res.status_code == 201


def test_description(whole_organism, testapp):
    res = testapp.patch_json(
        whole_organism['@id'],
        {'description': 'I am a modern major general.'})
    assert res.status_code == 200


def test_failure_patch_calculated_sex(whole_organism, testapp):
    res = testapp.patch_json(
        whole_organism['@id'],
        {'sex': 'female'}, expect_errors=True)
    assert res.status_code == 422


def test_collections(whole_organism, testapp):
    res = testapp.patch_json(
        whole_organism['@id'],
        {'collections': ['ENCODE']})
    assert res.status_code == 200
    res = testapp.patch_json(
        whole_organism['@id'],
        {'collections': ['ABBBCCCHD1455']}, expect_errors=True)
    assert res.status_code == 422


def test_sorted_from_detail_dependency(testapp, whole_organism, primary_cell):
    res = testapp.patch_json(
        whole_organism['@id'],
        {'sorted_from': primary_cell['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        whole_organism['@id'],
        {'sorted_from_detail': 'I am a sorted fraction detail.'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        whole_organism['@id'],
        {'sorted_from': primary_cell['@id'],
         'sorted_from_detail': 'I am a sorted fraction detail.'})
    assert res.status_code == 200


def test_not_required_properties(testapp, tissue, primary_cell, pooled_from_primary_cell, whole_organism):
    res = testapp.patch_json(
        whole_organism['@id'],
        {'part_of': tissue['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        whole_organism['@id'],
        {'pooled_from': [primary_cell['@id'],
                         pooled_from_primary_cell['@id']]
         }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        whole_organism['@id'],
        {'part_of': tissue['@id'],
         'pooled_from': [primary_cell['@id'],
                         pooled_from_primary_cell['@id']]
         }, expect_errors=True)
    assert res.status_code == 422
