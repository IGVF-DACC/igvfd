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
    principal_analysis_set,
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
        {'file_set': principal_analysis_set['@id']}
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
    tabular_file,
    curated_set_genome,
    assay_term_crispr,
    measurement_set,
    tissue
):
    testapp.patch_json(
        tabular_file['@id'],
        {'file_set': curated_set_genome['@id']}
    )
    testapp.patch_json(
        measurement_set['@id'],
        {'assay_term': assay_term_crispr['@id'],
         'samples': [tissue['@id']]}
    )
    testapp.patch_json(
        tissue['@id'],
        {'construct_library_sets': [construct_library_set_genome_wide['@id']]}
    )
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


def test_audit_construct_library_set_mpra_sequence_designs(
    testapp,
    construct_library_set_reporter,
    tabular_file,
    curated_set_genome,
    assay_term_mpra,
    measurement_set,
    tissue,
    assay_term_starr
):
    testapp.patch_json(
        tabular_file['@id'],
        {'file_set': curated_set_genome['@id']}
    )
    testapp.patch_json(
        measurement_set['@id'],
        {'assay_term': assay_term_mpra['@id'],
         'samples': [tissue['@id']]}
    )
    testapp.patch_json(
        tissue['@id'],
        {'construct_library_sets': [construct_library_set_reporter['@id']]}
    )
    res = testapp.get(construct_library_set_reporter['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing MPRA sequence designs'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        construct_library_set_reporter['@id'],
        {'integrated_content_files': [tabular_file['@id']]}
    )
    res = testapp.get(construct_library_set_reporter['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing MPRA sequence designs'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {'assay_term': assay_term_starr['@id']}
    )
    res = testapp.get(construct_library_set_reporter['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing MPRA sequence designs'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {'assay_term': assay_term_mpra['@id']}
    )
    testapp.patch_json(
        tabular_file['@id'],
        {'content_type': 'MPRA sequence designs'}
    )
    res = testapp.get(construct_library_set_reporter['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing MPRA sequence designs'
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


def test_audit_files_associated_with_incorrect_fileset_cls(testapp, base_expression_construct_library_set, configuration_file_seqspec, sequence_file):
    # Test 1: seqfiles file set != seqspec file set (audit)
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file['@id']],
            'file_set': base_expression_construct_library_set['@id']
        }
    )
    res = testapp.get(base_expression_construct_library_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing related files'
        for error in res.json['audit'].get('ERROR', [])
    )

    # Test 2: seqfiles file set == seqspec file set (no audit)
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': base_expression_construct_library_set['@id']
        }
    )
    res = testapp.get(base_expression_construct_library_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing related files'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_inconsistent_seqspec_cls(testapp, base_expression_construct_library_set, configuration_file_seqspec, configuration_file_seqspec_2, sequence_file, sequence_file_sequencing_run_2):
    # Test 1: seqfiles from the same set have different seqspecs (audit)
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': base_expression_construct_library_set['@id'],
            'illumina_read_type': 'R1',
            'sequencing_run': 1,
            'lane': 1
        }
    )
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file['@id']]
        }
    )
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'file_set': base_expression_construct_library_set['@id'],
            'illumina_read_type': 'R2',
            'sequencing_run': 1,
            'lane': 1
        }
    )
    testapp.patch_json(
        configuration_file_seqspec_2['@id'],
        {
            'seqspec_of': [sequence_file_sequencing_run_2['@id']]
        }
    )
    res = testapp.get(base_expression_construct_library_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent sequence specifications'
        for error in res.json['audit'].get('ERROR', [])
    )

    # Test 2: same seqspec linked to different sequence sets (no audit)
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'sequencing_run': 2
        }
    )
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file['@id'], sequence_file_sequencing_run_2['@id']]
        }
    )
    testapp.patch_json(
        configuration_file_seqspec_2['@id'],
        {
            'seqspec_of': [sequence_file['@id'], sequence_file_sequencing_run_2['@id']]
        }
    )
    res = testapp.get(base_expression_construct_library_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent sequence specifications'
        for error in res.json['audit'].get('ERROR', [])
    )

    # Test 3: when everything is correct
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'sequencing_run': 1
        }
    )
    res = testapp.get(base_expression_construct_library_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent sequence specifications'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_unexpected_seqspec_cls(testapp, sequence_file_pod5, sequence_file, configuration_file_seqspec, construct_library_set_genome_wide, base_expression_construct_library_set, experimental_protocol_document):
    # Test: If pod5, seqspec is unexpected (audit)
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file_pod5['@id']],
            'file_set': construct_library_set_genome_wide['@id']
        }
    )
    testapp.patch_json(
        sequence_file_pod5['@id'],
        {
            'file_set': construct_library_set_genome_wide['@id']
        }
    )
    res = testapp.get(construct_library_set_genome_wide['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected sequence specification'
        for error in res.json['audit'].get('ERROR', [])
    )
    # Patch: make a seqspec document
    testapp.patch_json(
        experimental_protocol_document['@id'],
        {
            'document_type': 'library structure seqspec',
        }
    )
    # Test: If double seqspec and non-single cell (audit)
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file['@id']],
            'file_set': base_expression_construct_library_set['@id']
        }
    )
    testapp.patch_json(
        sequence_file['@id'],
        {
            'seqspec_document': experimental_protocol_document['@id'],
            'file_set': base_expression_construct_library_set['@id']
        }
    )
    res = testapp.get(base_expression_construct_library_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected sequence specification'
        for error in res.json['audit'].get('ERROR', [])
    )
    # Test: If seqspec document is not a library structure seqspec (audit)
    testapp.patch_json(
        experimental_protocol_document['@id'],
        {
            'document_type': 'standards',
        }
    )
    res = testapp.get(base_expression_construct_library_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected sequence specification'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_missing_seqspec_cls(testapp, sequence_file, sequence_file_sequencing_run_2, experimental_protocol_document, configuration_file_seqspec, base_expression_construct_library_set):
    # Patch: make a seqspec document
    testapp.patch_json(
        experimental_protocol_document['@id'],
        {
            'document_type': 'library structure seqspec',
        }
    )
    # Test: SeqFiles without seqspec config or doc (audit)
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': base_expression_construct_library_set['@id']
        }
    )
    res = testapp.get(base_expression_construct_library_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing sequence specification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )

    # Test: SeqFile with seqspec doc (no audit)
    testapp.patch_json(
        sequence_file['@id'],
        {
            'seqspec_document': experimental_protocol_document['@id']
        }
    )
    res = testapp.get(base_expression_construct_library_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing sequence specification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )

    # Test: SeqFile with seqspec ConfigFile (no audit)
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'file_set': base_expression_construct_library_set['@id']
        }
    )
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'file_set': base_expression_construct_library_set['@id'],
            'seqspec_of': [sequence_file_sequencing_run_2['@id']]
        }
    )
    res = testapp.get(base_expression_construct_library_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing sequence specification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
