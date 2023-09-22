import pytest


def test_summary(testapp, multiplexed_sample, tissue, in_vitro_cell_line, human_tissue, multiplexed_sample_x2, multiplexed_sample_x3):
    res = testapp.get(multiplexed_sample['@id'])
    assert res.json.get(
        'summary') == 'multiplexed sample of K562 cell line, male, Mus musculus strain1, adrenal gland tissue, male, Mus musculus strain1'
    testapp.patch_json(
        multiplexed_sample['@id'],
        {
            'multiplexed_samples': [tissue['@id'], in_vitro_cell_line['@id'], human_tissue['@id']],
        }
    )
    res = testapp.get(multiplexed_sample['@id'])
    assert res.json.get(
        'summary') == 'multiplexed sample of K562 cell line, male, Mus musculus strain1, adrenal gland tissue, Homo sapiens, ... and 1 more sample'
    res = testapp.get(multiplexed_sample_x2['@id'])
    assert res.json.get(
        'summary') == 'multiplexed sample of K562 cell line, male, Mus musculus strain1, pluripotent stem cell, Homo sapiens, ... and 2 more samples'
    res = testapp.get(multiplexed_sample_x3['@id'])
    assert res.json.get(
        'summary') == 'multiplexed sample of K562 cell line, male, Mus musculus strain1, pluripotent stem cell, Homo sapiens, ... and 2 more samples'
