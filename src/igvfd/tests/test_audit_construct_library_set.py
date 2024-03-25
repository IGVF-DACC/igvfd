import pytest


def test_audit_construct_library_set_associated_phenotype(
    testapp,
    base_expression_construct_library_set
):
    # If 'phenotype-associated variants' appears in selection_criteria, the
    # associated_phenotypes property must be populated
    testapp.patch_json(
        base_expression_construct_library_set['@id'],
        {'selection_criteria': ['phenotype-associated variants']}
    )
    res = testapp.get(base_expression_construct_library_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing phenotype'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_construct_library_set_plasmid_map(
    testapp,
    base_expression_construct_library_set,
    plasmid_map_document
):
    # Every ConstructLibrarySet should have a "plasmid map" document in
    # the documents property
    res = testapp.get(base_expression_construct_library_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing plasmid map'
        for error in res.json['audit'].get('WARNING', [])
    )

    testapp.patch_json(
        base_expression_construct_library_set['@id'],
        {'documents': [plasmid_map_document['@id']]}
    )
    res = testapp.get(base_expression_construct_library_set['@id'] + '@@audit')
    assert 'missing plasmid map' not in (
        error['category'] for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_construct_library_set_exon_with_multiple_genes(
    testapp,
    base_expression_construct_library_set,
    gene_myc_hs, gene_CD1E,
    construct_library_set_tile
):
    # If the listed scope is "exon" or "tile", only 1 entry is expected in small_scale_gene_list property and large_scale_gene_list is not expected
    testapp.patch_json(
        base_expression_construct_library_set['@id'],
        {'small_scale_gene_list': [gene_CD1E['@id'], gene_myc_hs['@id']]}
    )
    res = testapp.get(base_expression_construct_library_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent scope'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        construct_library_set_tile['@id'],
        {'small_scale_gene_list': [gene_CD1E['@id'], gene_myc_hs['@id']]}
    )
    res = testapp.get(construct_library_set_tile['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent scope'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_construct_library_set_with_non_sequence_files(
    testapp,
    construct_library_set_genome_wide,
    analysis_set_with_sample,
    matrix_file
):
    testapp.patch_json(
        matrix_file['@id'],
        {'file_set': construct_library_set_genome_wide['@id']}
    )
    res = testapp.get(construct_library_set_genome_wide['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected file association'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        matrix_file['@id'],
        {'file_set': analysis_set_with_sample['@id']}
    )
    res = testapp.get(construct_library_set_genome_wide['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected file association'
        for error in res.json['audit'].get('WARNING', [])
    )
