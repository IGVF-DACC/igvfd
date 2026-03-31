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


def test_audit_pseudobulk_set_sample_matches_input(
    testapp,
    pseudobulk_set_base,
    analysis_set_base,
    measurement_set,
    primary_cell
):
    testapp.patch_json(
        analysis_set_base['@id'],
        {'input_file_sets': [measurement_set['@id']]}
    )
    testapp.patch_json(
        pseudobulk_set_base['@id'],
        {'input_file_sets': [analysis_set_base['@id']]}
    )
    res = testapp.get(pseudobulk_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent samples'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {'samples': [primary_cell['@id']]}
    )
    res = testapp.get(pseudobulk_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent samples'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_pseudobulk_set_input_file_set_type(
    testapp,
    pseudobulk_set_base,
    curated_set_genome,
    assay_term_scrna
):
    testapp.patch_json(
        pseudobulk_set_base['@id'],
        {'input_file_sets': [curated_set_genome['@id']]}
    )
    res = testapp.get(pseudobulk_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected input file set type'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        curated_set_genome['@id'],
        {
            'file_set_type': 'external sequencing data',
            'assay_term': assay_term_scrna['@id'],
            'preferred_assay_titles': ['10X multiome']
        }
    )
    res = testapp.get(pseudobulk_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected input file set type'
        for error in res.json['audit'].get('ERROR', [])
    )
