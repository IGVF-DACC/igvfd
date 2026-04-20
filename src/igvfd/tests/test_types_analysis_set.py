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


def test_assay_titles(testapp, analysis_set_base, measurement_set_mpra, measurement_set_multiome, principal_analysis_set, measurement_set_no_files, base_auxiliary_set, analysis_set_with_CLS_input, construct_library_set_reporter, primary_cell):
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


def test_analysis_set_summary(testapp, analysis_set_base, base_auxiliary_set, measurement_set_no_files, measurement_set_mpra, measurement_set_multiome, measurement_set_perturb_seq, principal_analysis_set, tabular_file, gene_myc_hs, assay_term_atac, assay_term_crispr, primary_cell, crispr_modification, construct_library_set_reporter, analysis_set_with_CLS_input, tissue, base_expression_construct_library_set, construct_library_set_editing_template_library, construct_library_set_editing_template_library_2, construct_library_set_reference_transduction, construct_library_set_non_targeting, multiplexed_sample, construct_library_set_genome_wide, curated_set_genome):
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
    measurement_set,
    measurement_set_multiome_2,
    in_vitro_organoid,
    in_vitro_differentiated_cell,
    in_vitro_cell_line,
    tissue,
    tissue_adipose,
    primary_cell,
    multiplexed_sample,
    sample_term_lymphoblastoid,
    phenotypic_feature_basic,
    phenotypic_feature_01,
    phenotypic_feature_digeorge_syndrome,
    phenotypic_feature_myocardial_infarction,
    human_donor,
    rodent_donor
):
    # Differentiated and cell line, non-disease feature
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [in_vitro_differentiated_cell['@id']]
        }
    )
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'phenotypic_features': [phenotypic_feature_basic['@id']],
            'classifications': ['differentiated cell specimen']
        }
    )
    curr_donor_acc = testapp.get(human_donor['@id']).json.get('accession')
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get(
        'sample_summary') == f'Human K562 differentiated to brown adipose tissue from donor {curr_donor_acc}'

    # Alzheimer's disease
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'phenotypic_features': [phenotypic_feature_01['@id']]
        }
    )
    curr_donor_acc = testapp.get(human_donor['@id']).json.get('accession')
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get(
        'sample_summary') == f'Human Alzheimer\'s disease K562 differentiated to brown adipose tissue from donor {curr_donor_acc}'

    # Reprogrammed and pooled
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'classifications': ['pooled cell specimen', 'reprogrammed cell specimen']
        }
    )
    curr_donor_acc = testapp.get(human_donor['@id']).json.get('accession')
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get(
        'sample_summary') == f'Human pooled Alzheimer\'s disease K562 reprogrammed to brown adipose tissue from donor {curr_donor_acc}'

    # Organoid
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [in_vitro_organoid['@id']]
        }
    )
    testapp.patch_json(
        in_vitro_organoid['@id'],
        {
            'classifications': ['organoid']
        }
    )
    curr_donor_acc = testapp.get(human_donor['@id']).json.get('accession')
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get(
        'sample_summary') == f'Human adrenal gland organoid from donor {curr_donor_acc}'

    # Gastruloid classification
    testapp.patch_json(
        in_vitro_organoid['@id'],
        {
            'classifications': ['gastruloid']
        }
    )
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get(
        'sample_summary') == f'Human adrenal gland gastruloid from donor {curr_donor_acc}'

    # Embryoid classification
    testapp.patch_json(
        in_vitro_organoid['@id'],
        {
            'classifications': ['embryoid']
        }
    )
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get(
        'sample_summary') == f'Human adrenal gland embryoid from donor {curr_donor_acc}'

    # Embryonic true
    testapp.patch_json(
        in_vitro_organoid['@id'],
        {
            'classifications': ['embryoid'],
            'embryonic': True
        }
    )
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get(
        'sample_summary') == f'Human embryonic adrenal gland embryoid from donor {curr_donor_acc}'

    # Tissue
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [tissue['@id']]
        }
    )
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get(
        'sample_summary') == 'Mouse adrenal gland tissue from strain1'

    # Tissue with disease phenotypic feature
    testapp.patch_json(
        tissue['@id'],
        {
            'phenotypic_features': [phenotypic_feature_01['@id']]
        }
    )
    res = testapp.get(principal_analysis_set['@id']).json
    curr_strain = testapp.get(rodent_donor['@id']).json.get('strain')
    assert res.get(
        'sample_summary') == f'Mouse Alzheimer\'s disease adrenal gland tissue from {curr_strain}'

    # Tissue with multiple disease phenotypic features
    testapp.patch_json(
        tissue['@id'],
        {
            'phenotypic_features': [phenotypic_feature_01['@id'],
                                    phenotypic_feature_basic['@id'],
                                    phenotypic_feature_digeorge_syndrome['@id'],
                                    phenotypic_feature_myocardial_infarction['@id']
                                    ]
        }
    )
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get(
        'sample_summary') == f'Mouse Alzheimer\'s disease and 2 other phenotypes adrenal gland tissue from {curr_strain}'

    # Primary cell
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
    curr_donor_acc = testapp.get(human_donor['@id']).json.get('accession')
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get(
        'sample_summary') == f'Human primary pluripotent stem cell from donor {curr_donor_acc}'

    # Multiple input file sets (human)
    testapp.patch_json(
        principal_analysis_set['@id'],
        {
            'input_file_sets': [measurement_set['@id'], measurement_set_multiome_2['@id']]
        }
    )
    testapp.patch_json(
        measurement_set_multiome_2['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [in_vitro_differentiated_cell['@id']]
        }
    )
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'phenotypic_features': [phenotypic_feature_basic['@id']]
        }
    )
    curr_donor_acc = testapp.get(human_donor['@id']).json.get('accession')
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get(
        'sample_summary', '') == f'Human pooled K562 reprogrammed to brown adipose tissue, primary pluripotent stem cell from donor {curr_donor_acc}'

    # Multiple input file sets (mouse)
    testapp.patch_json(
        measurement_set_multiome_2['@id'],
        {
            'samples': [tissue['@id']]
        }
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [tissue_adipose['@id']]
        }
    )
    testapp.patch_json(
        tissue['@id'],
        {
            'phenotypic_features': [phenotypic_feature_01['@id']]
        }
    )
    curr_tissue_donors = testapp.get(tissue['@id']).json.get('donors') + \
        testapp.get(tissue_adipose['@id']).json.get('donors')
    curr_tissue_strains = {testapp.get(donor['@id']).json.get('strain') for donor in curr_tissue_donors}
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get(
        'sample_summary', '') == f'Mouse adrenal gland tissue, brown adipose tissue from {len(curr_tissue_donors)} mice of {len(curr_tissue_strains)} strains'

    # Multiplexed sample
    testapp.patch_json(
        measurement_set['@id'],
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
            'sample_terms': [sample_term_lymphoblastoid['@id']]
        }
    )
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get('sample_summary', '') == 'Mixed species multiplexed sample of K562, lymphoblastoid cell line from 2 donors'

    # Multiplexed samples with multiple phenotypic features
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [multiplexed_sample['@id']]
        }
    )
    testapp.patch_json(
        multiplexed_sample['@id'],
        {
            'multiplexed_samples': [tissue['@id'],
                                    tissue_adipose['@id']]
        }
    )
    testapp.patch_json(
        tissue['@id'],
        {
            'phenotypic_features': [phenotypic_feature_01['@id'],
                                    phenotypic_feature_basic['@id'],
                                    phenotypic_feature_myocardial_infarction['@id']
                                    ]
        }
    )
    testapp.patch_json(
        tissue_adipose['@id'],
        {
            'phenotypic_features': [phenotypic_feature_01['@id'],
                                    phenotypic_feature_basic['@id'],
                                    phenotypic_feature_digeorge_syndrome['@id'],
                                    phenotypic_feature_myocardial_infarction['@id']
                                    ]
        }
    )
    curr_tissue_donors = testapp.get(tissue['@id']).json.get('donors') + \
        testapp.get(tissue_adipose['@id']).json.get('donors')
    curr_tissue_strains = {testapp.get(donor['@id']).json.get('strain') for donor in curr_tissue_donors}
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get(
        'sample_summary', '') == f'Mouse multiplexed sample of Alzheimer\'s disease and 2 other phenotypes adrenal gland tissue, brown adipose tissue from {len(curr_tissue_donors)} mice of {len(curr_tissue_strains)} strains'


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
