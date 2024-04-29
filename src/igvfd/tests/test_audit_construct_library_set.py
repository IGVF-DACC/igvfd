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
        error['category'] == 'missing associated phenotypes'
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
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )

    testapp.patch_json(
        base_expression_construct_library_set['@id'],
        {'documents': [plasmid_map_document['@id']]}
    )
    res = testapp.get(base_expression_construct_library_set['@id'] + '@@audit')
    assert 'missing plasmid map' not in (
        error['category'] for error in res.json['audit'].get('NOT_COMPLIANT', [])
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
        error['category'] == 'unexpected files'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        matrix_file['@id'],
        {'file_set': analysis_set_with_sample['@id']}
    )
    res = testapp.get(construct_library_set_genome_wide['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected files'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_construct_library_set_with_invalid_chroms(
    testapp,
    construct_library_set_genome_wide
):
    testapp.patch_json(
        construct_library_set_genome_wide['@id'],
        {'scope': 'loci',
         'small_scale_loci_list': [
             {
                 'assembly': 'GRCh38',
                 'chromosome': 'chr9',
                 'start': 1,
                 'end': 50
             },
             {
                 'assembly': 'GRCm39',
                 'chromosome': 'chr9',
                 'start': 1,
                 'end': 50
             }
         ]
         }
    )
    res = testapp.get(construct_library_set_genome_wide['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent loci'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        construct_library_set_genome_wide['@id'],
        {'small_scale_loci_list': [
            {
                'assembly': 'GRCh38',
                'chromosome': 'chrZ',
                'start': 1,
                'end': 50
            }
        ]
        }
    )
    res = testapp.get(construct_library_set_genome_wide['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent loci'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        construct_library_set_genome_wide['@id'],
        {'small_scale_loci_list': [
            {
                'assembly': 'GRCh38',
                'chromosome': 'chrX',
                'start': 1,
                'end': 156040896
            }
        ]
        }
    )
    res = testapp.get(construct_library_set_genome_wide['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent loci'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        construct_library_set_genome_wide['@id'],
        {'small_scale_loci_list': [
            {
                'assembly': 'GRCh38',
                'chromosome': 'chr9',
                'start': 1,
                'end': 50
            },
            {
                'assembly': 'GRCh38',
                'chromosome': 'chr9',
                'start': 75,
                'end': 125
            }
        ]
        }
    )
    res = testapp.get(construct_library_set_genome_wide['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent loci'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_construct_library_set_guide_library_guide_rna_sequences(
    testapp,
    construct_library_set_genome_wide,
    tabular_file
):
    res = testapp.get(construct_library_set_genome_wide['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing guide RNA sequences'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        construct_library_set_genome_wide['@id'],
        {'integrated_content_files': [tabular_file['@id']]}
    )
    res = testapp.get(construct_library_set_genome_wide['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing guide RNA sequences'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        tabular_file['@id'],
        {'content_type': 'guide RNA sequences'}
    )
    res = testapp.get(construct_library_set_genome_wide['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing guide RNA sequences'
        for error in res.json['audit'].get('NOT_COMPLIANT', []))


def test_audit_unexpected_virtual_sample(
    testapp,
    construct_library_set_genome_wide,
    tissue
):
    testapp.patch_json(
        tissue['@id'],
        {
            'construct_library_sets': [construct_library_set_genome_wide['@id']]
        }
    )
    res = testapp.get(construct_library_set_genome_wide['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected sample'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        tissue['@id'],
        {
            'virtual': True
        }
    )
    res = testapp.get(construct_library_set_genome_wide['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected sample'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_inconsistent_gene(
    testapp,
    construct_library_set_y2h,
    orf_foxp,
    orf_zscan10
):
    testapp.patch_json(
        construct_library_set_y2h['@id'],
        {
            'scope': 'interactors',
            'orf_list': [orf_foxp['@id'], orf_zscan10['@id']]
        }
    )
    res = testapp.get(construct_library_set_y2h['@id'] + '@@audit')
    assert all(
        error['category'] == 'inconsistent genes'
        for error in res.json['audit'].get('ERROR', [])
    )
