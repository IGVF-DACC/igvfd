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
