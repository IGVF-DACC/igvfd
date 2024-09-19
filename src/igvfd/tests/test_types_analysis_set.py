import pytest


def test_calculated_donors(testapp, analysis_set_base, primary_cell, human_donor, in_vitro_cell_line, rodent_donor):
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set([donor['@id'] for donor in res.json.get('donors')]) == {human_donor['@id']}
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'samples': [in_vitro_cell_line['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert set([donor['@id'] for donor in res.json.get('donors')]) == {rodent_donor['@id']}


def test_assay_titles(testapp, analysis_set_base, measurement_set_mpra, measurement_set_multiome, analysis_set_with_sample, measurement_set_no_files, base_auxiliary_set):
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
        analysis_set_with_sample['@id'],
        {
            'input_file_sets': [analysis_set_base['@id']]
        }
    )
    res = testapp.get(analysis_set_with_sample['@id'])
    assert set(res.json.get('assay_titles')) == {'10x multiome', 'lentiMPRA'}
    testapp.patch_json(
        measurement_set_no_files['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    testapp.patch_json(
        analysis_set_with_sample['@id'],
        {
            'input_file_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(analysis_set_with_sample['@id'])
    assert set(res.json.get('assay_titles')) == {'CRISPR FlowFISH screen'}


def test_analysis_set_summary(testapp, analysis_set_base, base_auxiliary_set, measurement_set_mpra, measurement_set_multiome, principal_analysis_set):
    # With no input_file_sets present, summary is based on analysis file_set_type only
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == 'intermediate analysis of data'
    # When no MeasurementSets (even nested in AnalysisSets) are present, data for other FileSet types are included in the summary
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == 'intermediate analysis of gRNA sequencing data'
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [base_auxiliary_set['@id'],
                                measurement_set_mpra['@id'],
                                measurement_set_multiome['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id']).json
    assert res.get('summary', '') == 'intermediate analysis of 10x multiome, MPRA data'
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
    assert res.get('summary', '') == 'intermediate analysis of 10x multiome, SUPERSTARR, lentiMPRA data'


def test_protocols(testapp, analysis_set_base, measurement_set_with_protocols):
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set_with_protocols['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'])
    assert res.json.get('protocols') == ['https://www.protocols.io/test-protocols-url-12345']


def test_analysis_set_sample_summary(testapp, analysis_set_with_sample, measurement_set_mpra, construct_library_set_genome_wide, sample_term_endothelial_cell, gene_myc_hs, treatment_chemical, in_vitro_differentiated_cell, in_vitro_cell_line):
    testapp.patch_json(
        analysis_set_with_sample['@id'],
        {
            'samples': [in_vitro_differentiated_cell['@id']]
        }
    )
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'construct_library_sets': [construct_library_set_genome_wide['@id']],
            'treatments': [treatment_chemical['@id']],
            'targeted_sample_term': sample_term_endothelial_cell['@id'],
            'sorted_from': in_vitro_cell_line['@id'],
            'sorted_from_detail': 'Example detail'

        }
    )
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'targeted_genes': [gene_myc_hs['@id']],
            'samples': [in_vitro_differentiated_cell['@id']]
        }
    )
    res = testapp.get(analysis_set_with_sample['@id']).json
    assert res.get('sample_summary', '') == 'K562 differentiated cell specimen induced to endothelial cell of vascular tree, differentiated with treatment(s), modified with a guide library, sorted on expression of MYC'
