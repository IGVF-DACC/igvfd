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


def test_summary(testapp, measurement_set, in_vitro_cell_line, assay_term_chip, modification_activation,
                 assay_term_crispr, primary_cell, modification, construct_library_set_reporter):
    res = testapp.get(measurement_set['@id'])
    assert res.json.get('summary') == 'STARR-seq'
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [in_vitro_cell_line['@id']],
            'readout': assay_term_chip['@id'],
            'preferred_assay_title': 'lentiMPRA'
        }
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'modifications': [modification_activation['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get('summary') == 'STARR-seq (lentiMPRA) followed by ChIP-seq'
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'construct_library_sets': [construct_library_set_reporter['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get(
        'summary') == 'STARR-seq (lentiMPRA) integrating a reporter library targeting accessible genome regions genome-wide followed by ChIP-seq'
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_crispr['@id']
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get(
        'summary') == 'CRISPR activation screen (lentiMPRA) integrating a reporter library targeting accessible genome regions genome-wide followed by ChIP-seq'
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [in_vitro_cell_line['@id'], primary_cell['@id']]
        }
    )
    testapp.patch_json(
        primary_cell['@id'],
        {
            'modifications': [modification['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert res.json.get(
        'summary') == 'mixed CRISPR screen (lentiMPRA) integrating a reporter library targeting accessible genome regions genome-wide followed by ChIP-seq'


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
