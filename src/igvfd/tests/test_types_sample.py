import pytest


def test_file_sets_link(testapp, tissue, measurement_set, analysis_set_base, curated_set_genome):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [tissue['@id']]
        }
    )
    res = testapp.get(tissue['@id'])
    assert res.json.get('file_sets') == [measurement_set['@id']]
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'samples': [tissue['@id']]
        }
    )
    testapp.patch_json(
        curated_set_genome['@id'],
        {
            'samples': [tissue['@id']]
        }
    )
    res = testapp.get(tissue['@id'])
    assert set(res.json.get('file_sets')) == set(
        [measurement_set['@id'], analysis_set_base['@id'], curated_set_genome['@id']])
