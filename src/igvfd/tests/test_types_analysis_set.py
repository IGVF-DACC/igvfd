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


def test_calculated_samples(testapp, measurement_set, analysis_set_base, primary_cell, human_donor, in_vitro_cell_line, multiplexed_sample):
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
        analysis_set_base['@id'],
        {
            'demultiplexed_sample': in_vitro_cell_line['@id']
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
    assert set(res.json.get('assay_titles')) == {'MPRA'}
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'preferred_assay_title': 'lentiMPRA'
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set(res.json.get('assay_titles')) == {'lentiMPRA'}
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set_mpra['@id'],
                                measurement_set_multiome['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set(res.json.get('assay_titles')) == {'10x multiome', 'lentiMPRA'}
    testapp.patch_json(
        principal_analysis_set['@id'],
        {
            'input_file_sets': [analysis_set_base['@id']]
        }
    )
    res = testapp.get(principal_analysis_set['@id'])
    assert set(res.json.get('assay_titles')) == {'10x multiome', 'lentiMPRA'}
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
    assert set(res.json.get('assay_titles')) == {'CRISPR FlowFISH screen'}
    testapp.patch_json(
        primary_cell['@id'],
        {
            'construct_library_sets': [construct_library_set_reporter['@id']]
        }
    )
    res = testapp.get(analysis_set_with_CLS_input['@id'])
    assert set(res.json.get('assay_titles')) == {'lentiMPRA'}


def test_analysis_set_summary(testapp, analysis_set_base, base_auxiliary_set, measurement_set_no_files, measurement_set_mpra, measurement_set_multiome, principal_analysis_set, tabular_file, gene_myc_hs, assay_term_atac, assay_term_crispr, primary_cell, crispr_modification, construct_library_set_reporter, analysis_set_with_CLS_input):
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
    assert res.get('summary', '') == 'Unspecified assay: peaks'
    # Case where the only input is an Auxiliary Set, which is not
    # linked to any Measurement Set.
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == 'Unspecified assay gRNA sequencing: peaks'
    # When no MeasurementSets (even nested in AnalysisSets) are present,
    # data for other FileSet types are included in the summary only if the
    # Measurement Set is not a CRISPR screen.
    testapp.patch_json(
        measurement_set_no_files['@id'],
        {
            'assay_term': assay_term_atac['@id'],
            'preferred_assay_title': 'ATAC-seq',
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
    assert res.get('summary', '') == 'ATAC-seq gRNA sequencing: peaks'
    # CRISPR screens do not mention the Aux Set file_set_type.
    # Also, modality appears in the summary.
    testapp.patch_json(
        measurement_set_no_files['@id'],
        {
            'assay_term': assay_term_crispr['@id'],
            'preferred_assay_title': 'CRISPR FlowFISH screen',
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == 'CRISPR FlowFISH screen: peaks'
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
            'modifications': [crispr_modification['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == '10x multiome, CRISPR interference FlowFISH screen, MPRA: peaks'
    # Preferred_assay_title of MeasurementSet is used instead of assay_term in summary whenever present
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'preferred_assay_title': 'lentiMPRA'
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
    assert res.get('summary', '') == 'interference 10x multiome, SUPERSTARR, lentiMPRA: peaks'
    # Display any targeted_genes from an input Measurement Set.
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'targeted_genes': [gene_myc_hs['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == 'interference 10x multiome, SUPERSTARR, lentiMPRA targeting MYC: peaks'
    testapp.patch_json(
        primary_cell['@id'],
        {
            'construct_library_sets': [construct_library_set_reporter['@id']]
        }
    )
    res = testapp.get(analysis_set_with_CLS_input['@id']).json
    assert res.get('summary', '') == 'lentiMPRA reporter library'


def test_protocols(testapp, analysis_set_base, measurement_set_with_protocols):
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set_with_protocols['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert res.json.get('protocols') == ['https://www.protocols.io/test-protocols-url-12345']


def test_analysis_set_sample_summary(testapp, principal_analysis_set, measurement_set_mpra, construct_library_set_genome_wide, sample_term_endothelial_cell, gene_myc_hs, treatment_chemical, in_vitro_differentiated_cell, in_vitro_cell_line, multiplexed_sample, crispr_modification, degron_modification, sample_term_lymphoblastoid):
    testapp.patch_json(
        principal_analysis_set['@id'],
        {
            'input_file_sets': [measurement_set_mpra['@id']]
        }
    )
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'construct_library_sets': [construct_library_set_genome_wide['@id']],
            'treatments': [treatment_chemical['@id']],
            'targeted_sample_term': sample_term_endothelial_cell['@id'],
            'sorted_from': in_vitro_cell_line['@id'],
            'sorted_from_detail': 'Example detail',
            'modifications': [crispr_modification['@id']]
        }
    )
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'targeted_genes': [gene_myc_hs['@id']],
            'samples': [in_vitro_differentiated_cell['@id']]
        }
    )
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get('sample_summary', '') == 'K562 differentiated cell specimen induced to endothelial cell of vascular tree, at 5 minute(s) post change, differentiated with 10 mM lactate for 1 hour, modified with CRISPRi Sp-dCas9, transfected with a guide library, sorted on expression of MYC'
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'modifications': [crispr_modification['@id'], degron_modification['@id']]
        }
    )
    res = testapp.get(principal_analysis_set['@id']).json
    assert res.get('sample_summary', '') == 'K562 differentiated cell specimen induced to endothelial cell of vascular tree, at 5 minute(s) post change, differentiated with 10 mM lactate for 1 hour, modified with AID system targeting MYC, CRISPRi Sp-dCas9, transfected with a guide library, sorted on expression of MYC'
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
    assert res.get('sample_summary', '') == 'multiplexed sample of K562, lymphoblastoid cell line and differentiated cell specimen, differentiated with 10 mM lactate for 1 hour, modified with AID system targeting MYC, CRISPRi Sp-dCas9, transfected with a guide library'


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


def test_workflows(testapp, analysis_set_with_workflow, matrix_file_with_base_workflow):
    '''Test to make sure that workflow is computed correctly.'''
    testapp.patch_json(
        matrix_file_with_base_workflow['@id'],
        {
            'file_set': analysis_set_with_workflow['@id']
        }
    )
    res = testapp.get(analysis_set_with_workflow['@id'])
    assert set([workflow['@id'] for workflow in res.json.get('workflows')]
               ) == {'/workflows/IGVFWF0000WRKF/'}
