import pytest


def test_audit_audit_pseudobulk_set_marker_gene_files(
    testapp,
    pseudobulk_set_base,
    tabular_file,
    reference_file
):
    res = testapp.get(pseudobulk_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing marker gene list'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        tabular_file['@id'],
        {'content_type': 'marker genes'}
    )
    res = testapp.get(pseudobulk_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing marker gene list'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
