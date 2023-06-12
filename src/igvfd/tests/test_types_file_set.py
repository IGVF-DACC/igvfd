import pytest


def test_files_link(testapp, sequence_file, reference_file, measurement_set):
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': measurement_set['@id']
        }
    )
    testapp.patch_json(
        reference_file['@id'],
        {
            'file_set': measurement_set['@id']
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert set(res.json.get('files')) == {sequence_file['@id'], reference_file['@id']}
    testapp.patch_json(
        sequence_file['@id'],
        {
            'status': 'deleted'
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert set(res.json.get('files')) == {reference_file['@id']}


def test_control_link(testapp, measurement_set, curated_set_genome):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'control_file_sets': [curated_set_genome['@id']]
        }
    )
    res = testapp.get(curated_set_genome['@id'])
    assert set(res.json.get('controlling_file_sets')) == {measurement_set['@id']}
