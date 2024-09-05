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
        analysis_set_base['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
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


def test_summary(testapp, measurement_set, in_vitro_cell_line, crispr_modification_activation, construct_library_set_reporter, phenotype_term_alzheimers, phenotype_term_myocardial_infarction, construct_library_set_genome_wide):
    res = testapp.get(measurement_set['@id'])
    assert res.json.get('summary') == 'SUPERSTARR'
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [in_vitro_cell_line['@id']],
            'preferred_assay_title': 'lentiMPRA'
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
            'preferred_assay_title': '10x multiome with MULTI-seq'
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
            'preferred_assay_title': 'CRISPR FlowFISH screen'
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get(
        'summary') == 'CRISPR activation FlowFISH screen integrating a reporter library targeting accessible genome regions genome-wide'
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
            'preferred_assay_title': 'scCRISPR screen'
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get(
        'summary') == 'scCRISPR activation screen integrating a guide (sgRNA) library targeting TF binding sites genome-wide associated with Alzheimer\'s disease and Myocardial infarction'


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
