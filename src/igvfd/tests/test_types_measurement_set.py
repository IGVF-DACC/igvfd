import pytest


def test_related_multiome_datasets(testapp, primary_cell, in_vitro_cell_line, measurement_set, measurement_set_multiome, measurement_set_multiome_2, analysis_set_base, curated_set_genome):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get('related_multiome_datasets') is None
    res = testapp.get(measurement_set_multiome['@id'])
    assert set([file_set_id['@id']
               for file_set_id in res.json.get('related_multiome_datasets')]) == {measurement_set['@id']}
    testapp.patch_json(
        curated_set_genome['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
    res = testapp.get(measurement_set_multiome['@id'])
    assert set([file_set_id['@id']
               for file_set_id in res.json.get('related_multiome_datasets')]) == {measurement_set['@id']}
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [in_vitro_cell_line['@id']]
        }
    )
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'samples': [in_vitro_cell_line['@id']],
            'multiome_size': 3
        }
    )
    testapp.patch_json(
        measurement_set_multiome_2['@id'],
        {
            'samples': [in_vitro_cell_line['@id']]
        }
    )
    res = testapp.get(measurement_set_multiome['@id'])
    assert set([file_set_id['@id'] for file_set_id in res.json.get('related_multiome_datasets')]
               ) == {measurement_set['@id'], measurement_set_multiome_2['@id']}


def test_summary(testapp, measurement_set, in_vitro_cell_line, crispr_modification_activation, construct_library_set_reporter, phenotype_term_alzheimers, phenotype_term_myocardial_infarction, construct_library_set_genome_wide, assay_term_y2h, construct_library_set_reference_transduction, multiplexed_sample):
    res = testapp.get(measurement_set['@id'])
    assert res.json.get('summary') == 'STARR-seq'
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [in_vitro_cell_line['@id']],
            'preferred_assay_titles': ['lentiMPRA']
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get('summary') == 'lentiMPRA'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'construct_library_sets': [construct_library_set_reporter['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get(
        'summary') == 'lentiMPRA integrating a reporter library targeting accessible genome regions genome-wide'
    testapp.patch_json(
        measurement_set['@id'],
        {
            'preferred_assay_titles': ['10x multiome with MULTI-seq']
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get(
        'summary') == 'STARR-seq (10x multiome with MULTI-seq) integrating a reporter library targeting accessible genome regions genome-wide'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'modifications': [crispr_modification_activation['@id']]
        }
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'preferred_assay_titles': ['CRISPR FlowFISH screen']
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get(
        'summary') == 'CRISPR FlowFISH screen integrating a reporter library targeting accessible genome regions genome-wide'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'construct_library_sets': [construct_library_set_genome_wide['@id']]
        }
    )
    testapp.patch_json(
        construct_library_set_genome_wide['@id'],
        {
            'associated_phenotypes': [phenotype_term_alzheimers['@id'], phenotype_term_myocardial_infarction['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get(
        'summary') == 'CRISPR activation FlowFISH screen integrating a guide (sgRNA) library targeting TF binding sites genome-wide associated with Alzheimer\'s disease and Myocardial infarction'
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_y2h['@id'],
            'preferred_assay_titles': ['Arrayed yN2H']
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get(
        'summary') == 'post-selection CRISPR activation Arrayed yN2H integrating a guide (sgRNA) library targeting TF binding sites genome-wide associated with Alzheimer\'s disease and Myocardial infarction'
    testapp.patch_json(
        measurement_set['@id'],
        {
            'control_types': ['reference transduction', 'non-targeting'],
            'preferred_assay_titles': ['scCRISPR screen'],
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get(
        'summary') == 'non-targeting, reference transduction scCRISPR activation screen integrating a guide (sgRNA) library targeting TF binding sites genome-wide associated with Alzheimer\'s disease and Myocardial infarction'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'construct_library_sets': [construct_library_set_reference_transduction['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get(
        'summary') == 'non-targeting scCRISPR screen integrating a reference transduction expression vector library'
    testapp.patch_json(
        construct_library_set_reference_transduction['@id'],
        {
            'control_types': ['reference transduction', 'non-targeting']
        }
    )
    # Test inclusion of multiplexing_methods from samples.
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [multiplexed_sample['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get(
        'summary') == 'scCRISPR screen (barcode based multiplexed) integrating a non-targeting, reference transduction expression vector library'


def test_summary_targeted_genes(testapp, measurement_set, assay_term_chip, assay_term_CRISPR_sorted, gene_myc_hs, gene_zscan10_mm, gene_CRLF2_par_y, gene_CD1E, gene_TAB3_AS1, gene_MAGOH2P):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_chip['@id'],
            'targeted_genes': [gene_myc_hs['@id']],
            'preferred_assay_titles': ['Histone ChIP-seq']
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get('summary') == 'Histone ChIP-seq targeting MYC'
    testapp.patch_json(
        measurement_set['@id'],
        {
            'targeted_genes': [gene_myc_hs['@id'], gene_zscan10_mm['@id'], gene_CRLF2_par_y['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get('summary') == 'Histone ChIP-seq targeting CRLF2, MYC, Zcan10'
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_CRISPR_sorted['@id'],
            'preferred_assay_titles': ['CRISPR FACS screen']
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get('summary') == 'CRISPR FACS screen sorted on the expression of CRLF2, MYC, Zcan10'
    testapp.patch_json(
        measurement_set['@id'],
        {
            'targeted_genes': [gene_myc_hs['@id'], gene_zscan10_mm['@id'], gene_CRLF2_par_y['@id'], gene_CD1E['@id'], gene_TAB3_AS1['@id'], gene_MAGOH2P['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get('summary') == 'CRISPR FACS screen sorted on the expression of 6 genes'


def test_calculated_donors(testapp, measurement_set, primary_cell, human_donor, in_vitro_cell_line, rodent_donor):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert set([donor['@id'] for donor in res.json.get('donors')]) == {human_donor['@id']}
    testapp.patch_json(
        primary_cell['@id'],
        {
            'donors': [human_donor['@id'], rodent_donor['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert set([donor['@id'] for donor in res.json.get('donors')]) == {human_donor['@id'], rodent_donor['@id']}
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [in_vitro_cell_line['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert set([donor['@id'] for donor in res.json.get('donors')]) == {rodent_donor['@id']}


def test_calculated_externally_hosted(testapp, measurement_set, sequence_file):
    res = testapp.get(measurement_set['@id'])
    assert res.json.get('externally_hosted') == False
    testapp.patch_json(
        sequence_file['@id'],
        {
            'externally_hosted': True,
            'external_host_url': 'https://tested_url',
            'file_set': measurement_set['@id']
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get('externally_hosted') == True


def test_calculated_controlled_access_data_use_limitations(testapp, measurement_set, in_vitro_cell_line, institutional_certificate, institutional_certificate_controlled, other_lab, lab):
    # IC is not of the same lab.
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [in_vitro_cell_line['@id']]
        }
    )
    testapp.patch_json(
        institutional_certificate['@id'],
        {
            'samples': [in_vitro_cell_line['@id']],
            'lab': other_lab['@id']
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert 'controlled_access' not in res.json
    assert res.json.get('data_use_limitation_summaries') == ['no certificate']
    # Add the lab of Measurement set as a partner lab.
    testapp.patch_json(
        institutional_certificate['@id'],
        {
            'partner_labs': [lab['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get('controlled_access') == False
    assert res.json.get('data_use_limitation_summaries') == ['No limitations']
    # Add another IC for other lab, without partner labs.
    # Calculated props should be the same as before.
    testapp.patch_json(
        institutional_certificate_controlled['@id'],
        {
            'samples': [in_vitro_cell_line['@id']],
            'lab': other_lab['@id']
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get('controlled_access') == False
    assert res.json.get('data_use_limitation_summaries') == ['No limitations']
    # Change 2nd IC to the right lab. Calculated props
    # should change now.
    testapp.patch_json(
        institutional_certificate_controlled['@id'],
        {
            'lab': lab['@id']
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get('controlled_access') == True
    assert set(res.json.get('data_use_limitation_summaries')) == set(['GRU', 'No limitations'])
