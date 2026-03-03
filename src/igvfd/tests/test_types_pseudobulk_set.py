import pytest


def test_pseudobulk_set_summary(testapp, pseudobulk_set_base, in_vitro_cell_line):
    # Case 1: Pseudobulk's source biosample is not a cell line.
    res = testapp.get(pseudobulk_set_base['@id']).json
    assert res.get('summary', '') == 'Pseudobulk of adrenal gland endothelial cell of vascular tree'
    # Case 2: Pseudobulk's source biosample is a cell line. Also, include cell_qualifier.
    testapp.patch_json(
        pseudobulk_set_base['@id'],
        {
            'samples': [in_vitro_cell_line['@id']],
            'cell_qualifier': 'exhausted'
        }
    )
    res = testapp.get(pseudobulk_set_base['@id']).json
    assert res.get('summary', '') == 'Pseudobulk of exhausted endothelial cell of vascular tree derived from K562'
