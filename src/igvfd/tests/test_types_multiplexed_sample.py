import pytest


def test_summary(testapp, multiplexed_sample, tissue, in_vitro_cell_line, human_tissue, multiplexed_sample_x2, multiplexed_sample_x3):
    res = testapp.get(multiplexed_sample['@id'])
    assert res.json.get(
        'summary') == 'multiplexed sample: Mus musculus strain1 (male) K562 cell line; Mus musculus strain1 (male) adrenal gland tissue'
    testapp.patch_json(
        multiplexed_sample['@id'],
        {
            'multiplexed_samples': [tissue['@id'], in_vitro_cell_line['@id'], human_tissue['@id']],
        }
    )
    res = testapp.get(multiplexed_sample['@id'])
    assert res.json.get(
        'summary') == 'multiplexed sample: Mus musculus strain1 (male) K562 cell line; Homo sapiens adrenal gland tissue; ... and 1 more sample'
    res = testapp.get(multiplexed_sample_x2['@id'])
    assert res.json.get(
        'summary') == 'multiplexed sample: Mus musculus strain1 (male) K562 cell line; Homo sapiens pluripotent stem cell; ... and 2 more samples'
    res = testapp.get(multiplexed_sample_x3['@id'])
    assert res.json.get(
        'summary') == 'multiplexed sample: Mus musculus strain1 (male) K562 cell line; Homo sapiens pluripotent stem cell; ... and 2 more samples'


def test_taxa(testapp, multiplexed_sample_mixed_species, multiplexed_sample):
    res = testapp.get(multiplexed_sample_mixed_species['@id'])
    assert res.json.get('taxa') == 'Mixed species'
    res = testapp.get(multiplexed_sample['@id'])
    assert res.json.get('taxa') == 'Mus musculus'
