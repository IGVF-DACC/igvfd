import pytest


def test_multiplexed_sample_summary(testapp, multiplexed_sample, tissue, in_vitro_cell_line, human_tissue, primary_cell, sample_term_endothelial_cell, in_vitro_differentiated_cell, in_vitro_organoid, sample_term_brown_adipose_tissue, sample_term_lymphoblastoid):
    # Test: 2 samp types, same donor
    res = testapp.get(multiplexed_sample['@id'])
    assert res.json.get(
        'summary') == 'multiplexed K562 and adrenal gland, 1 donor, 2 samples'

    # Test: 2 samp types, different donors
    testapp.patch_json(
        multiplexed_sample['@id'],
        {
            'multiplexed_samples': [tissue['@id'], in_vitro_cell_line['@id'], human_tissue['@id']],
        }
    )
    res = testapp.get(multiplexed_sample['@id'])
    assert res.json.get(
        'summary') == 'multiplexed K562 and adrenal gland, 2 donors, 3 samples'

    # Test: 4 samp types, different donors, 4 samples
    testapp.patch_json(
        multiplexed_sample['@id'],
        {
            'multiplexed_samples': [tissue['@id'], in_vitro_cell_line['@id'], human_tissue['@id'], primary_cell['@id']],
        }
    )
    res = testapp.get(multiplexed_sample['@id'])
    assert res.json.get(
        'summary') == 'multiplexed K562, adrenal gland and pluripotent stem cell, 2 donors, 4 samples'

    # Test: 4 samp types, different donors, 6 samples, 2 targeted sample terms
    testapp.patch_json(
        multiplexed_sample['@id'],
        {
            'multiplexed_samples': [
                tissue['@id'],
                in_vitro_cell_line['@id'],
                human_tissue['@id'],
                primary_cell['@id'],
                in_vitro_differentiated_cell['@id'],
                in_vitro_organoid['@id']
            ]
        }
    )
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'sample_terms': [sample_term_brown_adipose_tissue['@id']]
        }
    )
    testapp.patch_json(
        in_vitro_organoid['@id'],
        {
            'sample_terms': [sample_term_lymphoblastoid['@id']]
        }
    )
    testapp.patch_json(
        human_tissue['@id'],
        {
            'sample_terms': [sample_term_endothelial_cell['@id']]
        }
    )
    res = testapp.get(multiplexed_sample['@id'])
    assert res.json.get(
        'summary') == 'multiplexed K562, adrenal gland, brown adipose tissue, endothelial cell of vascular tree and 1 more, 2 donors, 6 samples, induced to adrenal gland and brown adipose tissue'

    # Test: 4 samp types, different donors, 6 samples, 1 targeted sample term
    testapp.patch_json(
        multiplexed_sample['@id'],
        {
            'multiplexed_samples': [
                tissue['@id'],
                in_vitro_cell_line['@id'],
                human_tissue['@id'],
                primary_cell['@id'],
                in_vitro_differentiated_cell['@id']
            ]
        }
    )
    res = testapp.get(multiplexed_sample['@id'])
    assert res.json.get(
        'summary') == 'multiplexed K562, adrenal gland, brown adipose tissue, endothelial cell of vascular tree and pluripotent stem cell, 2 donors, 5 samples, induced to brown adipose tissue'


def test_taxa(testapp, multiplexed_sample_mixed_species, multiplexed_sample):
    res = testapp.get(multiplexed_sample_mixed_species['@id'])
    assert res.json.get('taxa') == 'Mixed species'
    res = testapp.get(multiplexed_sample['@id'])
    assert res.json.get('taxa') == 'Mus musculus'
