import pytest


def test_summary(testapp, multiplexed_sample, tissue, in_vitro_cell_line, human_tissue):
    res = testapp.get(multiplexed_sample['@id'])
    assert res.json.get(
        'summary') == 'multiplexed sample of K562 cell line, male Mus musculus strain1, adrenal gland tissue, male Mus musculus strain1'
    testapp.patch_json(
        multiplexed_sample['@id'],
        {
            'multiplexed_samples': [tissue['@id'], in_vitro_cell_line['@id'], human_tissue['@id']],
        }
    )
    res = testapp.get(multiplexed_sample['@id'])
    assert res.json.get(
        'summary') == 'multiplexed sample of K562 cell line, male Mus musculus strain1, adrenal gland tissue, Homo sapiens, ... and 1 more sample'
