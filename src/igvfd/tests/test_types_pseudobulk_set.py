import pytest


def test_pseudobulk_set_summary(testapp, pseudobulk_set_base, in_vitro_cell_line):
    # With no input_file_sets and no files present, summary is based on analysis file_set_type only.
    res = testapp.get(pseudobulk_set_base['@id']).json
    assert res.get('summary', '') == 'Pseudobulk of adrenal gland endothelial cell of vascular tree'
    # When there are files, but no input_file_sets, summary says Unspecified.
    testapp.patch_json(
        pseudobulk_set_base['@id'],
        {
            'samples': [in_vitro_cell_line['@id']],
            'cell_qualifier': 'exhausted'
        }
    )
    res = testapp.get(pseudobulk_set_base['@id']).json
    assert res.get('summary', '') == 'Pseudobulk of exhausted endothelial cell of vascular tree derived from K562'
