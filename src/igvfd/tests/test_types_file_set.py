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
