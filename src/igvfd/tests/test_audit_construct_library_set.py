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
        error['category'] == 'inconsistent variants and phenotype metadata'
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
    construct_library_set_tile,
    construct_library_set_genome_wide,
    tabular_file
):
    # If the listed scope is "exon" or "tile", only 1 entry is expected in small_scale_gene_list property and large_scale_gene_list is not expected
    testapp.patch_json(
        base_expression_construct_library_set['@id'],
        {'small_scale_gene_list': [gene_CD1E['@id'], gene_myc_hs['@id']]}
    )
    res = testapp.get(base_expression_construct_library_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent scope metadata'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        construct_library_set_tile['@id'],
        {'small_scale_gene_list': [gene_CD1E['@id'], gene_myc_hs['@id']]}
    )
    res = testapp.get(construct_library_set_tile['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent scope metadata'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        construct_library_set_genome_wide['@id'],
        {'large_scale_gene_list': tabular_file['@id'],
         'scope': 'exon',
         'exon': 'E2'}
    )
    res = testapp.get(construct_library_set_tile['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent scope metadata'
        for error in res.json['audit'].get('WARNING', [])
    )
