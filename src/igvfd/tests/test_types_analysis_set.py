import pytest


def test_calculated_donors(testapp, measurement_set, analysis_set_base, primary_cell, human_donor, in_vitro_cell_line, rodent_donor):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set([donor['@id'] for donor in res.json.get('donors')]) == {human_donor['@id']}
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [in_vitro_cell_line['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set([donor['@id'] for donor in res.json.get('donors')]) == {rodent_donor['@id']}


def test_calculated_samples(testapp, measurement_set, analysis_set_base, construct_library_set_genome_wide, tissue, primary_cell, in_vitro_cell_line, multiplexed_sample):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set([sample['@id'] for sample in res.json.get('samples')]) == {primary_cell['@id']}
    testapp.patch_json(
        tissue['@id'],
        {
            'construct_library_sets': [construct_library_set_genome_wide['@id']]
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set['@id'], construct_library_set_genome_wide['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set([sample['@id'] for sample in res.json.get('samples')]) == {primary_cell['@id']}
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'demultiplexed_samples': [in_vitro_cell_line['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set([sample['@id'] for sample in res.json.get('samples')]) == {primary_cell['@id']}
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [multiplexed_sample['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set([sample['@id'] for sample in res.json.get('samples')]) == {in_vitro_cell_line['@id']}


def test_assay_titles(testapp, analysis_set_base, measurement_set_mpra, measurement_set_multiome, principal_analysis_set, measurement_set_no_files, base_auxiliary_set, analysis_set_with_CLS_input, construct_library_set_reporter, primary_cell, curated_set_genome):
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set_mpra['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set(res.json.get('preferred_assay_titles')) == {'MPRA'}
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'preferred_assay_titles': ['lentiMPRA']
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set(res.json.get('preferred_assay_titles')) == {'lentiMPRA'}
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set_mpra['@id'],
                                measurement_set_multiome['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set(res.json.get('preferred_assay_titles')) == {'10x multiome', 'lentiMPRA'}
    testapp.patch_json(
        principal_analysis_set['@id'],
        {
            'input_file_sets': [analysis_set_base['@id']]
        }
    )
    res = testapp.get(principal_analysis_set['@id'])
    assert set(res.json.get('preferred_assay_titles')) == {'10x multiome', 'lentiMPRA'}
    testapp.patch_json(
        measurement_set_no_files['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    testapp.patch_json(
        principal_analysis_set['@id'],
        {
            'input_file_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(principal_analysis_set['@id'])
    assert set(res.json.get('preferred_assay_titles')) == {'CRISPR FlowFISH screen'}
    testapp.patch_json(
        primary_cell['@id'],
        {
            'construct_library_sets': [construct_library_set_reporter['@id']]
        }
    )
    res = testapp.get(analysis_set_with_CLS_input['@id'])
    assert set(res.json.get('preferred_assay_titles')) == {'lentiMPRA'}
    assert set(res.json.get('assay_titles')) == {'massively parallel reporter assay'}
    res = testapp.get(construct_library_set_reporter['@id'])
    assert set(res.json.get('preferred_assay_titles')) == {'lentiMPRA'}
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set_mpra['@id'], construct_library_set_reporter['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set(res.json.get('preferred_assay_titles')) == {'lentiMPRA'}
    assert set(res.json.get('assay_titles')) == {'massively parallel reporter assay'}
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [construct_library_set_reporter['@id'], curated_set_genome['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set(res.json.get('preferred_assay_titles')) == {'lentiMPRA'}
    assert set(res.json.get('assay_titles')) == {'massively parallel reporter assay'}
    cls_curated_intermediate = testapp.post_json(
        '/analysis_set',
        {
            'award': analysis_set_with_CLS_input['award'],
            'lab': analysis_set_with_CLS_input['lab'],
            'file_set_type': 'intermediate analysis',
            'input_file_sets': [construct_library_set_reporter['@id'], curated_set_genome['@id']],
        },
        status=201,
    ).json['@graph'][0]
    res = testapp.get(cls_curated_intermediate['@id'])
    assert set(res.json.get('preferred_assay_titles')) == {'lentiMPRA'}
    assert set(res.json.get('assay_titles')) == {'massively parallel reporter assay'}
    downstream_mpra = testapp.post_json(
        '/analysis_set',
        {
            'award': analysis_set_with_CLS_input['award'],
            'lab': analysis_set_with_CLS_input['lab'],
            'file_set_type': 'intermediate analysis',
            'input_file_sets': [cls_curated_intermediate['@id'], measurement_set_mpra['@id']],
        },
        status=201,
    ).json['@graph'][0]
    res = testapp.get(downstream_mpra['@id'])
    assert set(res.json.get('preferred_assay_titles')) == {'lentiMPRA'}
    assert set(res.json.get('assay_titles')) == {'massively parallel reporter assay'}
    measurement_set_scqer = testapp.post_json(
        '/measurement_set',
        {
            'award': measurement_set_mpra['award'],
            'lab': measurement_set_mpra['lab'],
            'assay_term': measurement_set_mpra['assay_term'],
            'samples': [primary_cell['@id']],
            'file_set_type': 'experimental data',
            'preferred_assay_titles': ['MPRA (scQer)'],
        },
        status=201,
    ).json['@graph'][0]
    res = testapp.get(construct_library_set_reporter['@id'])
    assert set(res.json.get('preferred_assay_titles')) == {'MPRA (scQer)', 'lentiMPRA'}
    res = testapp.get(analysis_set_with_CLS_input['@id'])
    assert set(res.json.get('preferred_assay_titles')) == {'MPRA (scQer)', 'lentiMPRA'}
    downstream_scqer = testapp.post_json(
        '/analysis_set',
        {
            'award': analysis_set_with_CLS_input['award'],
            'lab': analysis_set_with_CLS_input['lab'],
            'file_set_type': 'intermediate analysis',
            'input_file_sets': [analysis_set_with_CLS_input['@id'], measurement_set_scqer['@id']],
        },
        status=201,
    ).json['@graph'][0]
    res = testapp.get(downstream_scqer['@id'])
    assert set(res.json.get('preferred_assay_titles')) == {'MPRA (scQer)'}
    assert set(res.json.get('assay_titles')) == {'massively parallel reporter assay'}
    downstream_cls_only = testapp.post_json(
        '/analysis_set',
        {
            'award': analysis_set_with_CLS_input['award'],
            'lab': analysis_set_with_CLS_input['lab'],
            'file_set_type': 'intermediate analysis',
            'input_file_sets': [analysis_set_with_CLS_input['@id']],
        },
        status=201,
    ).json['@graph'][0]
    res = testapp.get(downstream_cls_only['@id'])
    assert set(res.json.get('preferred_assay_titles')) == {'MPRA (scQer)', 'lentiMPRA'}
    assert set(res.json.get('assay_titles')) == {'massively parallel reporter assay'}


def test_assay_titles_curated_set_inputs(
    testapp,
    analysis_set_base,
    curated_set_genome,
    curated_set_external_sequencing,
    construct_library_set_reporter,
    primary_cell,
    measurement_set_mpra,
):
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [curated_set_genome['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert res.json.get('preferred_assay_titles') is None
    assert res.json.get('assay_titles') is None

    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [curated_set_external_sequencing['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set(res.json.get('preferred_assay_titles')) == {'RNA-seq'}

    testapp.patch_json(
        primary_cell['@id'],
        {
            'construct_library_sets': [construct_library_set_reporter['@id']]
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [
                curated_set_external_sequencing['@id'],
                construct_library_set_reporter['@id'],
            ]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set(res.json.get('preferred_assay_titles')) == {'RNA-seq'}


def test_analysis_set_summary(testapp, analysis_set_base, base_auxiliary_set, measurement_set_no_files, measurement_set_mpra, measurement_set_multiome, measurement_set_perturb_seq, principal_analysis_set, tabular_file, gene_myc_hs, assay_term_atac, assay_term_crispr, primary_cell, crispr_modification, construct_library_set_reporter, analysis_set_with_CLS_input, tissue, base_expression_construct_library_set, construct_library_set_editing_template_library, construct_library_set_editing_template_library_2, construct_library_set_reference_transduction, construct_library_set_non_targeting, multiplexed_sample, construct_library_set_genome_wide, curated_set_genome, curated_set_external_sequencing):
    # With no input_file_sets and no files present, summary is based on analysis file_set_type only.
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == 'Unspecified assay'
    # When there are files, but no input_file_sets, summary says Unspecified.
    testapp.patch_json(
        tabular_file['@id'],
        {
            'file_set': analysis_set_base['@id']
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == 'Unspecified assay'
    # Case where the only input is an Auxiliary Set, which is not
    # linked to any Measurement Set.
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == 'Unspecified assay gRNA sequencing'
    # When no MeasurementSets (even nested in AnalysisSets) are present,
    # data for other FileSet types are included in the summary only if the
    # Measurement Set is not a CRISPR screen.
    testapp.patch_json(
        measurement_set_no_files['@id'],
        {
            'assay_term': assay_term_atac['@id'],
            'preferred_assay_titles': ['ATAC-seq'],
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == 'ATAC-seq gRNA sequencing'
    # CRISPR screens do not mention the Aux Set file_set_type.
    # Also, modality appears in the summary.
    testapp.patch_json(
        measurement_set_no_files['@id'],
        {
            'assay_term': assay_term_crispr['@id'],
            'preferred_assay_titles': ['CRISPR FlowFISH screen'],
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == 'CRISPR FlowFISH screen'
    # Mixed input file sets with Auxiliary Set and Measurement Set
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [base_auxiliary_set['@id'],
                                measurement_set_mpra['@id'],
                                measurement_set_multiome['@id']]
        }
    )
    testapp.patch_json(
        primary_cell['@id'],
        {
            'modifications': [crispr_modification['@id']],
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == 'ATAC-seq (10x multiome), CRISPR FlowFISH screen, MPRA'
    testapp.patch_json(
        primary_cell['@id'],
        {
            'construct_library_sets': [construct_library_set_genome_wide['@id']],
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == 'ATAC-seq (10x multiome), CRISPR interference FlowFISH screen, MPRA integrating a guide (sgRNA) library targeting TF binding sites genome-wide'
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'samples': [primary_cell['@id']],
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == 'ATAC-seq (10x multiome), CRISPR interference FlowFISH screen, MPRA integrating a guide (sgRNA) library targeting TF binding sites genome-wide'
    # Preferred_assay_title of MeasurementSet is used instead of assay_term in summary whenever present
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'preferred_assay_titles': ['lentiMPRA']
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set_mpra['@id'],
                                measurement_set_multiome['@id'],
                                principal_analysis_set['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == 'CRISPR interference ATAC-seq (10x multiome), STARR-seq, lentiMPRA integrating a guide (sgRNA) library targeting TF binding sites genome-wide'
    # Display any targeted_genes from an input Measurement Set.
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'targeted_genes': [gene_myc_hs['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == 'CRISPR interference ATAC-seq (10x multiome), STARR-seq, lentiMPRA targeting MYC integrating a guide (sgRNA) library targeting TF binding sites genome-wide'
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'control_types': ['low FACS signal']
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get(
        'summary', '') == 'CRISPR interference ATAC-seq (10x multiome), STARR-seq, lentiMPRA targeting MYC integrating a guide (sgRNA) library targeting TF binding sites genome-wide with low FACS signal control'
    testapp.patch_json(
        measurement_set_perturb_seq['@id'],
        {
            'control_types': ['untransfected']
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set_mpra['@id'],
                                measurement_set_multiome['@id'],
                                measurement_set_perturb_seq['@id'],
                                principal_analysis_set['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get(
        'summary', '') == 'CRISPR interference ATAC-seq (10x multiome), Perturb-seq, STARR-seq, lentiMPRA targeting MYC integrating a guide (sgRNA) library targeting TF binding sites genome-wide with low FACS signal, untransfected controls'
    # Test inclusion of the multiplexing method.
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'samples': [multiplexed_sample['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get(
        'summary', '') == 'CRISPR interference ATAC-seq (10x multiome), Perturb-seq, STARR-seq, lentiMPRA (barcode based multiplexed) targeting MYC integrating a guide (sgRNA) library targeting TF binding sites genome-wide with low FACS signal, untransfected controls'
    # Analysis Set that has construct_library_sets but the input_file_sets is a Measurement Set.
    testapp.patch_json(
        primary_cell['@id'],
        {
            'construct_library_sets': [construct_library_set_reporter['@id']]
        }
    )
    testapp.patch_json(
        analysis_set_with_CLS_input['@id'],
        {
            'input_file_sets': [measurement_set_mpra['@id']]
        }
    )
    res = testapp.get(analysis_set_with_CLS_input['@id']).json
    assert res.get('summary', '') == 'lentiMPRA targeting MYC integrating a reporter library targeting accessible genome regions genome-wide with low FACS signal control'
    # Analysis Set with only a CLS (and curated set) in input_file_sets.
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [construct_library_set_reporter['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get(
        'summary', '') == 'lentiMPRA reporter library targeting accessible genome regions genome-wide'
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [construct_library_set_reporter['@id'], curated_set_genome['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get(
        'summary', '') == 'lentiMPRA reporter library targeting accessible genome regions genome-wide'
    # Construct library sets should not contribute to the summary unless the samples are transfected with it
    testapp.patch_json(
        analysis_set_with_CLS_input['@id'],
        {
            'input_file_sets': [measurement_set_multiome['@id'], construct_library_set_reporter['@id']]
        }
    )
    res = testapp.get(analysis_set_with_CLS_input['@id']).json
    assert res.get('summary', '') == 'ATAC-seq (10x multiome) (barcode based multiplexed)'
    testapp.patch_json(
        tissue['@id'],
        {
            'construct_library_sets': [construct_library_set_reporter['@id']]
        }
    )
    res = testapp.get(analysis_set_with_CLS_input['@id']).json
    assert res.get(
        'summary', '') == 'ATAC-seq (10x multiome) (barcode based multiplexed) integrating a reporter library targeting accessible genome regions genome-wide'
    testapp.patch_json(
        tissue['@id'],
        {
            'construct_library_sets': [construct_library_set_reporter['@id'], base_expression_construct_library_set['@id']]
        }
    )
    res = testapp.get(analysis_set_with_CLS_input['@id']).json
    assert res.get('summary', '') == 'ATAC-seq (10x multiome) (barcode based multiplexed) integrating an expression vector library of exon E3 of MYC and a reporter library targeting accessible genome regions genome-wide'
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'control_types': ['non-targeting']
        }
    )
    testapp.patch_json(
        tissue['@id'],
        {
            'construct_library_sets': [construct_library_set_reference_transduction['@id']]
        }
    )
    res = testapp.get(analysis_set_with_CLS_input['@id']).json
    assert res.get(
        'summary', '') == 'ATAC-seq (10x multiome) (barcode based multiplexed) integrating a reference transduction expression vector library with non-targeting control'
    testapp.patch_json(
        tissue['@id'],
        {
            'construct_library_sets': [construct_library_set_reference_transduction['@id'], construct_library_set_non_targeting['@id']]
        }
    )
    res = testapp.get(analysis_set_with_CLS_input['@id']).json
    assert res.get('summary', '') == 'CRISPR ATAC-seq (10x multiome) (barcode based multiplexed) integrating a non-targeting guide (sgRNA) library and a reference transduction expression vector library'
    # when > 2 editing template libraries: display counts
    testapp.patch_json(
        construct_library_set_reporter['@id'],
        {
            'file_set_type': 'editing template library',
            'scope': 'targeton',
            'small_scale_gene_list': [gene_myc_hs['@id']],
            'targeton': 'targeton3',
            'selection_criteria': [
                'sequence variants'
            ]
        }
    )
    testapp.patch_json(
        construct_library_set_editing_template_library['@id'],
        {
            'selection_criteria': [
                'sequence variants'
            ]
        }
    )
    testapp.patch_json(
        tissue['@id'],
        {
            'construct_library_sets': [construct_library_set_editing_template_library['@id'], construct_library_set_editing_template_library_2['@id'], construct_library_set_reporter['@id']]
        }
    )
    res = testapp.get(analysis_set_with_CLS_input['@id']).json
    assert res.get(
        'summary', '') == 'ATAC-seq (10x multiome) (barcode based multiplexed) integrating editing template libraries targeting sequence variants in 3 targetons of MYC with non-targeting control'
    # Case where the input curated set has file_set_type 'external sequencing data', and has assay_term and preferred_assay_titles specified.
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [curated_set_external_sequencing['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == 'RNA-seq'


def test_analysis_set_protocols(testapp, analysis_set_base, measurement_set_with_protocols):
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set_with_protocols['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert res.json.get('protocols') == ['https://www.protocols.io/private/test-protocols-url-12345']


def test_analysis_set_sample_summary(
    testapp,
    principal_analysis_set,
    analysis_set_base,
    measurement_set_mpra,
    measurement_set_one_onlist,
    measurement_set_perturb_seq,
    measurement_set,
    sample_term_endothelial_cell,
    in_vitro_differentiated_cell,
    in_vitro_cell_line,
    in_vitro_organoid,
    in_vitro_system_virtual_demultiplexed,
    tissue,
    tissue_parkinsons,
    multiplexed_sample,
    technical_sample,
    sample_term_lymphoblastoid,
    sample_term_K562,
    sample_term_brown_adipose_tissue,
    sample_term_gastrula,
    sample_term_technical_sample,
    phenotypic_feature_basic,
    phenotypic_feature_01,
    rodent_donor,
    parent_rodent_donor_1,
    parent_rodent_donor_2,
    human_donor,
    parent_human_donor_1,
    parent_human_donor_2,
    construct_library_set_overexpression,
    base_expression_construct_library_set,
    experimental_protocol_document
):
    # Test group 1: non-multiplexed samples with various metadata
    testapp.patch_json(
        principal_analysis_set['@id'],
        {
            'input_file_sets': [measurement_set_mpra['@id']]
        }
    )
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'samples': [in_vitro_differentiated_cell['@id']]
        }
    )

    # Test group 1: targeted sample terms (human donor)
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'targeted_sample_term': sample_term_endothelial_cell['@id'],
        }
    )
    res = testapp.get(principal_analysis_set['@id']).json
    hs_donor_accession = testapp.get(human_donor['@id']).json.get('accession')
    assert res.get('sample_summary',
                   '') == f'human K562 differentiated cell specimen induced to endothelial cell of vascular tree at 5 minute(s) post change from donor(s) {hs_donor_accession}'

    # Test group 1: new classifications (change wording)
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'classifications': ['pooled cell specimen', 'differentiated cell specimen']
        }
    )
    res = testapp.get(principal_analysis_set['@id']).json
    hs_donor_accession = testapp.get(human_donor['@id']).json.get('accession')
    assert res.get(
        'sample_summary', '') == f'human K562 pooled differentiated cell specimen induced to endothelial cell of vascular tree at 5 minute(s) post change from donor(s) {hs_donor_accession}'

    # Test group 1: add disease terms with targeted term
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'phenotypic_features': [phenotypic_feature_basic['@id'],
                                    phenotypic_feature_01['@id']]
        }
    )
    # note: per portal data, NCIT is disease term if there is no measurement linked
    testapp.patch_json(
        phenotypic_feature_basic['@id'],
        {
            'quality': 'unknown'
        }
    )
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get(
        'sample_summary', '') == f'human K562 pooled differentiated cell specimen with Alzheimer\'s disease induced to endothelial cell of vascular tree at 5 minute(s) post change from donor(s) {hs_donor_accession}'

    # Test group 1: add overexpression CLS
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'construct_library_sets': [construct_library_set_overexpression['@id']]
        }
    )
    res = testapp.get(principal_analysis_set['@id']).json
    hs_donor_accession = testapp.get(human_donor['@id']).json.get('accession')
    assert res.get('sample_summary',
                   '') == f'human K562 pooled differentiated cell specimen with Alzheimer\'s disease induced to endothelial cell of vascular tree at 5 minute(s) post change from donor(s) {hs_donor_accession}, overexpressing MYC'

    # Test group 1: add disease without targeted term
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'samples': [tissue['@id']]
        }
    )
    testapp.patch_json(
        tissue['@id'],
        {
            'phenotypic_features': [phenotypic_feature_basic['@id'],
                                    phenotypic_feature_01['@id']]
        }
    )
    res = testapp.get(principal_analysis_set['@id']).json
    ms_donor_accession = testapp.get(rodent_donor['@id']).json.get('accession')
    assert res.get(
        'sample_summary', '') == f'mouse adrenal gland tissue/organ with Alzheimer\'s disease from {ms_donor_accession} mice of strain1 strain(s)'

    # Test group 1: multiple human donors
    testapp.patch_json(
        tissue['@id'],
        {
            'donors': [parent_human_donor_1['@id'], human_donor['@id'], parent_human_donor_2['@id']]
        }
    )
    hs_donor_accession_1 = testapp.get(parent_human_donor_1['@id']).json.get('accession')
    hs_donor_accession_2 = testapp.get(parent_human_donor_2['@id']).json.get('accession')
    hs_donor_accessions = testapp.get(human_donor['@id']).json.get('accession')
    sorted_hs_donors = sorted([hs_donor_accession_1, hs_donor_accession_2, hs_donor_accessions])
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get(
        'sample_summary', '') == f'human adrenal gland tissue/organ with Alzheimer\'s disease from donor(s) {sorted_hs_donors[0]}, {sorted_hs_donors[1]} and 1 more'

    # Test group 1: multiple human donors
    testapp.patch_json(
        tissue['@id'],
        {
            'donors': [rodent_donor['@id'], parent_rodent_donor_1['@id'], parent_rodent_donor_2['@id']]
        }
    )
    ms_donor_accession_1 = testapp.get(parent_rodent_donor_1['@id']).json.get('accession')
    ms_donor_accession_2 = testapp.get(parent_rodent_donor_2['@id']).json.get('accession')
    ms_donor_accessions = testapp.get(rodent_donor['@id']).json.get('accession')
    sorted_ms_donors = sorted([ms_donor_accession_1, ms_donor_accession_2, ms_donor_accessions])
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get(
        'sample_summary', '') == f'mouse adrenal gland tissue/organ with Alzheimer\'s disease from {sorted_ms_donors[0]}, {sorted_ms_donors[1]} and 1 more mice of strain1, strain2, and 1 more strain(s)'

    # Test group 2: multiplexed samples
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'samples': [multiplexed_sample['@id']]
        }
    )
    testapp.patch_json(
        multiplexed_sample['@id'],
        {
            'multiplexed_samples': [in_vitro_differentiated_cell['@id'], in_vitro_cell_line['@id']]
        }
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'sample_terms': [sample_term_lymphoblastoid['@id']],
        }
    )
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get('sample_summary',
                   '') == 'mixed species multiplexed sample of K562 with Alzheimer\'s disease, lymphoblastoid cell line from 1 human donor(s), 1 mouse donor(s), overexpressing MYC'

    # Test group 2: disease info
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'phenotypic_features': [phenotypic_feature_basic['@id']]
        }
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'phenotypic_features': [phenotypic_feature_basic['@id'],
                                    phenotypic_feature_01['@id']]
        }
    )
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get('sample_summary',
                   '') == 'mixed species multiplexed sample of K562, lymphoblastoid cell line with Alzheimer\'s disease from 1 human donor(s), 1 mouse donor(s), overexpressing MYC'

    # Test group 3: Corces PD special collection
    testapp.patch_json(
        principal_analysis_set['@id'],
        {
            'collections': ['PD single cell multiomics']
        }
    )
    testapp.patch_json(
        multiplexed_sample['@id'],
        {
            'multiplexed_samples': [tissue['@id'], tissue_parkinsons['@id']]
        }
    )
    testapp.patch_json(
        tissue['@id'],
        {
            'donors': [parent_human_donor_1['@id']]
        }
    )
    res = testapp.get(principal_analysis_set['@id']).json
    hs_donor_accession_1 = testapp.get(parent_human_donor_1['@id']).json.get('accession')
    hs_donor_accessions = testapp.get(human_donor['@id']).json.get('accession')
    sorted_hs_donors = sorted([hs_donor_accession_1, hs_donor_accessions])
    assert res.get('sample_summary',
                   '') == f'Parkinson\'s collection of human multiplexed sample of adrenal gland, middle temporal gyrus with and without Parkinson\'s from donor(s) {sorted_hs_donors[0]} and {sorted_hs_donors[1]}'

    # Test group 4: non-mux samples with multiple target terms and times (test concat)
    # Starting fresh
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set['@id'],
                                measurement_set_one_onlist['@id'],
                                measurement_set_perturb_seq['@id']
                                ],
            'file_set_type': 'principal analysis'
        }
    )
    # target sample 1 (K562 to gastrula)
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [in_vitro_differentiated_cell['@id']]
        }
    )
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'targeted_sample_term': sample_term_gastrula['@id'],
            'donors': [human_donor['@id']],
            'classifications': ['differentiated cell specimen'],
            'phenotypic_features': [phenotypic_feature_basic['@id']],
            'construct_library_sets': [base_expression_construct_library_set['@id']]
        }
    )
    # target sample 2 (K562 to brown adipose tissue)
    testapp.patch_json(
        measurement_set_one_onlist['@id'],
        {
            'samples': [in_vitro_cell_line['@id']]
        }
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'targeted_sample_term': sample_term_brown_adipose_tissue['@id'],
            'donors': [human_donor['@id']],
            'sample_terms': [sample_term_K562['@id']],
            'classifications': ['differentiated cell specimen'],
            'cell_fate_change_protocol': experimental_protocol_document['@id'],
            'time_post_change': 10,
            'time_post_change_units': 'minute',
            'phenotypic_features': [phenotypic_feature_basic['@id']]
        }
    )
    # target sample 3 (K562 to lymphoblastoid cell line)
    testapp.patch_json(
        measurement_set_perturb_seq['@id'],
        {
            'samples': [in_vitro_organoid['@id']]
        }
    )
    testapp.patch_json(
        in_vitro_organoid['@id'],
        {
            'targeted_sample_term': sample_term_lymphoblastoid['@id'],
            'donors': [human_donor['@id']],
            'sample_terms': [sample_term_K562['@id']],
            'classifications': ['differentiated cell specimen'],
            'cell_fate_change_protocol': experimental_protocol_document['@id'],
            'time_post_change': 2,
            'time_post_change_units': 'minute',
        }
    )
    hs_donor_accession = testapp.get(human_donor['@id']).json.get('accession')
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get(
        'sample_summary', '') == f'human K562 differentiated cell specimen induced to brown adipose tissue, gastrula, lymphoblastoid cell line at 2 minute, 5 minute, 10 minute(s) post change from donor(s) {hs_donor_accession}'

    # Test group 5: technical samples (no donors)
    testapp.patch_json(
        sample_term_technical_sample['@id'],
        {
            'term_name': 'cell'
        }
    )
    testapp.patch_json(
        technical_sample['@id'],
        {
            'taxa': 'Saccharomyces cerevisiae'
        }
    )
    testapp.patch_json(
        measurement_set_perturb_seq['@id'],
        {
            'samples': [technical_sample['@id']]
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set_perturb_seq['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get(
        'sample_summary', '') == 'yeast cell technical sample'

    # Test group 6: sample term and classifications overlap (cell line)
    testapp.patch_json(
        sample_term_K562['@id'],
        {
            'term_name': 'K562 cell'
        }
    )
    testapp.patch_json(
        in_vitro_system_virtual_demultiplexed['@id'],
        {
            'virtual': False
        }
    )
    testapp.patch_json(
        measurement_set_perturb_seq['@id'],
        {
            'samples': [in_vitro_system_virtual_demultiplexed['@id']]
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set_perturb_seq['@id']]
        }
    )
    hs_donor_accession = testapp.get(human_donor['@id']).json.get('accession')
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get(
        'sample_summary', '') == f'human K562 cell line from donor(s) {hs_donor_accession}'

    # Test group 7: have biosample qualifiers
    testapp.patch_json(
        in_vitro_system_virtual_demultiplexed['@id'],
        {
            'biosample_qualifiers': ['exhausted']
        }
    )
    hs_donor_accession = testapp.get(human_donor['@id']).json.get('accession')
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get(
        'sample_summary', '') == f'human exhausted K562 cell line from donor(s) {hs_donor_accession}'


def test_functional_assay_mechanisms(testapp, analysis_set_base, measurement_set, measurement_set_with_functional_assay_mechanisms, phenotype_term_from_go, phenotype_term_myocardial_infarction):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'functional_assay_mechanisms': [phenotype_term_from_go['@id'], phenotype_term_myocardial_infarction['@id']]
        }

    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set_with_functional_assay_mechanisms['@id'], measurement_set['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set([mechanism['@id'] for mechanism in res.json.get('functional_assay_mechanisms')]
               ) == {phenotype_term_from_go['@id'], phenotype_term_myocardial_infarction['@id']}


def test_types_analysis_set_test_workflows(testapp, analysis_set_with_workflow, matrix_file_with_base_workflow, analysis_step_version):
    '''Test to make sure that workflow is computed correctly.'''
    testapp.patch_json(
        matrix_file_with_base_workflow['@id'],
        {
            'file_set': analysis_set_with_workflow['@id']
        }
    )
    res = testapp.get(analysis_set_with_workflow['@id'])
    assert set(
        workflow['@id']
        for workflow in res.json.get('workflows')
    ) == {'/workflows/IGVFWF0000WRKF/'}


def test_targeted_genes(testapp, measurement_set, analysis_set_base, gene_myc_hs):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'targeted_genes': [gene_myc_hs['@id']]
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set([gene['@id'] for gene in res.json.get('targeted_genes')]) == {gene_myc_hs['@id']}


def test_analysis_set_targeted_proteins(testapp, measurement_set, analysis_set_base, assay_term_chip, lab, award, tissue):
    '''
    Calculated `targeted_proteins`, `summary` targeting phrase, union across measurement sets,
    and propagation when an analysis set is the input of another analysis set.
    '''
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_chip['@id'],
            'targeted_proteins': ['H3K4me3'],
            'preferred_assay_titles': ['Histone ChIP-seq']
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert res.json.get('targeted_proteins') == ['H3K4me3']
    assert res.json.get('summary') == 'Histone ChIP-seq targeting H3K4me3'

    ms_a = testapp.post_json(
        '/measurement_set',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'assay_term': assay_term_chip['@id'],
            'samples': [tissue['@id']],
            'file_set_type': 'experimental data',
            'preferred_assay_titles': ['Histone ChIP-seq'],
            'targeted_proteins': ['H3K27ac'],
        },
        status=201,
    ).json['@graph'][0]
    ms_b = testapp.post_json(
        '/measurement_set',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'assay_term': assay_term_chip['@id'],
            'samples': [tissue['@id']],
            'file_set_type': 'experimental data',
            'preferred_assay_titles': ['Histone ChIP-seq'],
            'targeted_proteins': ['H3K4me3', 'IgG'],
        },
        status=201,
    ).json['@graph'][0]
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [ms_a['@id'], ms_b['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert res.json.get('targeted_proteins') == ['H3K27ac', 'H3K4me3', 'IgG']
    assert res.json.get('summary') == 'Histone ChIP-seq targeting H3K27ac, H3K4me3, IgG'

    ms_nested = testapp.post_json(
        '/measurement_set',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'assay_term': assay_term_chip['@id'],
            'samples': [tissue['@id']],
            'file_set_type': 'experimental data',
            'preferred_assay_titles': ['Histone ChIP-seq'],
            'targeted_proteins': ['IgG'],
        },
        status=201,
    ).json['@graph'][0]
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [ms_nested['@id']]
        }
    )
    principal_analysis_set = testapp.post_json(
        '/analysis_set',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'file_set_type': 'principal analysis',
            'input_file_sets': [analysis_set_base['@id']],
        },
        status=201,
    ).json['@graph'][0]
    res = testapp.get(principal_analysis_set['@id'])
    assert res.json.get('targeted_proteins') == ['IgG']
    assert res.json.get('summary') == 'Histone ChIP-seq targeting IgG'


def test_enrichment_designs(testapp, measurement_set, analysis_set_base, tabular_file):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'enrichment_designs': [tabular_file['@id']]
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set(res.json.get('enrichment_designs')) == {tabular_file['@id']}
    assert res.json.get('summary') == (
        'STARR-seq enriched for a targeted gene expression panel'
    )
