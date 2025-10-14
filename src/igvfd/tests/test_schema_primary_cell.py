import pytest


def test_sample_1(primary_cell, testapp):
    res = testapp.get(primary_cell['@id'])
    assert res.json['accession'][:6] == 'IGVFSM'


def test_lot_id_dependency(primary_cell, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert res.status_code == 422


def test_product_id_dependency(award, lab, source, rodent_donor, sample_term_pluripotent_stem_cell, testapp):
    res = testapp.post_json(
        '/primary_cell',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'product_id': '700',
            'donors': [rodent_donor['@id']],
            'sample_terms': [sample_term_pluripotent_stem_cell['@id']]
        },
        expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/primary_cell',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'sources': [source['@id']],
            'product_id': '700',
            'donors': [rodent_donor['@id']],
            'sample_terms': [sample_term_pluripotent_stem_cell['@id']]
        })
    assert res.status_code == 201


def test_pooled_from(primary_cell, tissue, pooled_from_primary_cell, pooled_from_primary_cell_2, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'pooled_from': [pooled_from_primary_cell['@id']]}, expect_errors=True)
    assert (res.status_code == 422)
    res = testapp.patch_json(
        primary_cell['@id'],
        {'pooled_from': [pooled_from_primary_cell['@id'], tissue['@id']]}, expect_errors=True)
    assert (res.status_code == 422)
    res = testapp.patch_json(
        primary_cell['@id'],
        {'pooled_from': [pooled_from_primary_cell['@id'], pooled_from_primary_cell_2['@id']]})
    assert (res.status_code == 200)


def test_collections(primary_cell, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'collections': ['ENCODE']})
    assert res.status_code == 200
    res = testapp.patch_json(
        primary_cell['@id'],
        {'collections': ['ABBBCCCHD1455']}, expect_errors=True)
    assert res.status_code == 422


def test_part_of_primary_cell(primary_cell, primary_cell_part_of, in_vitro_differentiated_cell, in_vitro_organoid, in_vitro_cell_line, tissue_part_of, whole_organism_part_of, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'part_of': in_vitro_differentiated_cell['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        primary_cell['@id'],
        {'part_of': in_vitro_organoid['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        primary_cell['@id'],
        {'part_of': in_vitro_cell_line['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        primary_cell['@id'],
        {'part_of':  primary_cell_part_of['@id']})
    assert res.status_code == 200
    res = testapp.patch_json(
        primary_cell['@id'],
        {'part_of':  tissue_part_of['@id']})
    assert res.status_code == 200
    res = testapp.patch_json(
        primary_cell['@id'],
        {'part_of':  whole_organism_part_of['@id']})
    assert res.status_code == 200


def test_sorted_from_detail_dependency(testapp, primary_cell):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'sorted_from': primary_cell['@id']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        primary_cell['@id'],
        {'sorted_from_detail': 'I am a sorted fraction detail.'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        primary_cell['@id'],
        {'sorted_from': primary_cell['@id'],
         'sorted_from_detail': 'I am a sorted fraction detail.'})
    assert res.status_code == 200


def test_patch_virtual(primary_cell, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'virtual': True})
    assert res.status_code == 200
    res = testapp.patch_json(
        primary_cell['@id'],
        {'virtual': False})
    assert res.status_code == 200
    res = testapp.patch_json(
        primary_cell['@id'],
        {'virtual': ''}, expect_errors=True)
    assert res.status_code == 422


def test_primary_cell_protocols_regex(primary_cell, testapp):
    res = testapp.patch_json(
        primary_cell['@id'],
        {'protocols': ['https://www.protocols.io/123/ABC']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        primary_cell['@id'],
        {'protocols': ['https://www.protocols.io/123/ABC', 'https://www.protocols.io/private/123/ABC']}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        primary_cell['@id'],
        {'protocols': ['https://www.protocols.io/private/123/ABC']})
    assert res.status_code == 200
    res = testapp.patch_json(
        primary_cell['@id'],
        {'protocols': ['https://www.protocols.io/view/123/ABC']})
    assert res.status_code == 200
