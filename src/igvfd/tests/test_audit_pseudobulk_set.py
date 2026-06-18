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
    pseudobulk_set_merged,
    analysis_set_base,
    measurement_set,
    primary_cell,
    multiplexed_sample
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
    # Input file set's sample is a multiplexed sample
    testapp.patch_json(
        measurement_set['@id'],
        {'samples': [multiplexed_sample['@id']]}
    )
    res = testapp.get(pseudobulk_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent samples'
        for error in res.json['audit'].get('ERROR', [])
    )
    # Merged Pseudobulk Set
    res = testapp.get(pseudobulk_set_merged['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent samples'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        pseudobulk_set_base['@id'],
        {'samples': [primary_cell['@id']]}
    )
    res = testapp.get(pseudobulk_set_merged['@id'] + '@@audit')
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
            'preferred_assay_titles': ['10x multiome']
        }
    )
    res = testapp.get(pseudobulk_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected input file set type'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_pseudobulk_set_mixed_classifications(
    testapp,
    pseudobulk_set_base,
    tissue,
    tissue_parkinsons,
    in_vitro_cell_line,
    sample_term_adrenal_gland
):
    res = testapp.get(pseudobulk_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent parent samples'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        pseudobulk_set_base['@id'],
        {'samples': [tissue['@id'], in_vitro_cell_line['@id']]}
    )
    res = testapp.get(pseudobulk_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent parent samples'
        for error in res.json['audit'].get('WARNING', [])
    )
    # Same classification, different terms
    testapp.patch_json(
        pseudobulk_set_base['@id'],
        {'samples': [tissue['@id'], tissue_parkinsons['@id']]}
    )
    res = testapp.get(pseudobulk_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent parent samples'
        for error in res.json['audit'].get('WARNING', [])
    )
    # Same classification, same term
    testapp.patch_json(
        tissue_parkinsons['@id'],
        {'sample_terms': [sample_term_adrenal_gland['@id']]}
    )
    res = testapp.get(pseudobulk_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent parent samples'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_pseudobulk_set_mismatched_merged_cell_types(
    testapp,
    pseudobulk_set_merged,
    pseudobulk_set_2,
    pseudobulk_set_base,
    sample_term_endothelial_cell
):
    res = testapp.get(pseudobulk_set_merged['@id'] + '@@audit')
    assert any(
        error['category'] == 'mismatched merged cell types'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        pseudobulk_set_2['@id'],
        {'cell_type': sample_term_endothelial_cell['@id']}
    )
    res = testapp.get(pseudobulk_set_merged['@id'] + '@@audit')
    assert all(
        error['category'] != 'mismatched merged cell types'
        for error in res.json['audit'].get('WARNING', [])
    )
