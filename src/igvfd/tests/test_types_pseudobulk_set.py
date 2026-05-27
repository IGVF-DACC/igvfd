import pytest


def test_pseudobulk_set_summary(testapp, pseudobulk_set_base, in_vitro_cell_line):
    res = testapp.get(pseudobulk_set_base['@id']).json
    assert res.get('summary', '') == 'Pseudobulk of endothelial cell of vascular tree derived from adrenal gland'
    # Cell qualifier appears before the cell type.
    testapp.patch_json(
        pseudobulk_set_base['@id'],
        {
            'samples': [in_vitro_cell_line['@id']],
            'cell_qualifier': 'exhausted'
        }
    )
    res = testapp.get(pseudobulk_set_base['@id']).json
    assert res.get('summary', '') == 'Pseudobulk of exhausted endothelial cell of vascular tree derived from K562'


def test_pseudobulk_set_donors(
    testapp,
    pseudobulk_set_base,
    in_vitro_cell_line,
    rodent_donor,
):
    testapp.patch_json(
        pseudobulk_set_base['@id'],
        {
            'samples': [in_vitro_cell_line['@id']]
        }
    )

    res = testapp.get(pseudobulk_set_base['@id']).json

    assert {donor['@id']
            for donor in res.get('donors', [])
            } == {rodent_donor['@id']}

    testapp.patch_json(
        rodent_donor['@id'],
        {
            'status': 'deleted'
        }
    )
    res = testapp.get(pseudobulk_set_base['@id'])
    assert res.json.get('donors') is None


def test_pseudobulk_set_cell_annotation(testapp, pseudobulk_set_base, in_vitro_cell_line, sample_term_K562):
    res = testapp.get(pseudobulk_set_base['@id']).json
    assert res.get('cell_annotation', '') == 'adrenal gland endothelial cell of vascular tree'
    # Cell qualifier appears before the cell type.
    testapp.patch_json(
        pseudobulk_set_base['@id'],
        {
            'cell_qualifier': 'exhausted'
        }
    )
    res = testapp.get(pseudobulk_set_base['@id']).json
    assert res.get('cell_annotation', '') == 'adrenal gland exhausted endothelial cell of vascular tree'
    # Pseudobulks with cell line source biosamples

    testapp.patch_json(
        pseudobulk_set_base['@id'],
        {
            'samples': [in_vitro_cell_line['@id']]
        }
    )
    res = testapp.get(pseudobulk_set_base['@id']).json
    assert res.get('cell_annotation', '') == 'exhausted endothelial cell of vascular tree derived from K562'
    # Pseudobulk where cell type is the same as the source biosample
    testapp.patch_json(
        pseudobulk_set_base['@id'],
        {
            'cell_type': sample_term_K562['@id']
        }
    )
    res = testapp.get(pseudobulk_set_base['@id']).json
    assert res.get('cell_annotation', '') == 'exhausted K562'
