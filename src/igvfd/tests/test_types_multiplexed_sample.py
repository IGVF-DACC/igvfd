import pytest


def test_summary(testapp, multiplexed_sample, tissue, in_vitro_cell_line, whole_organism):
    res = testapp.get(multiplexed_sample['@id'])
    tissue_summary = testapp.get(tissue['@id']).json.get('summary')
    in_vitro_cell_line_summary = testapp.get(in_vitro_cell_line['@id']).json.get('summary')
    assert in_vitro_cell_line_summary in res.json.get(
        'summary') and tissue_summary in res.json.get('summary')
    testapp.patch_json(
        multiplexed_sample['@id'],
        {
            'multiplexed_samples': [tissue['@id'], in_vitro_cell_line['@id'], whole_organism['@id']],
        }
    )
    whole_organism_summary = testapp.get(whole_organism['@id']).json.get('summary')
    res = testapp.get(multiplexed_sample['@id'])
    assert res.json.get('summary').endswith(', ... and 1 more sample')
    assert sum(1 for summary in [tissue_summary, in_vitro_cell_line_summary,
               whole_organism_summary] if summary in res.json.get('summary')) == 2
