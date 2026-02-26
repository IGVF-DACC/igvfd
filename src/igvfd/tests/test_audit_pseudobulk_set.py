import pytest


def test_audit_pseudobulk_set_marker_gene_files(
    testapp,
    pseudobulk_set_base,
    analysis_set_base,
    tabular_file
):
    testapp.patch_json(
        pseudobulk_set_base['@id'],
        {'input_file_sets': [analysis_set_base['@id']]}
    )
    res = testapp.get(pseudobulk_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing marker gene list'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        tabular_file['@id'],
        {
            'file_set': analysis_set_base['@id'],
            'content_type': 'marker genes'
        }
    )
    res = testapp.get(pseudobulk_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing marker gene list'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
