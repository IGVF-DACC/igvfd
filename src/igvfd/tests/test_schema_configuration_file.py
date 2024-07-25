import pytest


def test_seqspec_of_dependency(testapp, configuration_file_json, sequence_file):
    res = testapp.patch_json(
        configuration_file_json['@id'],
        {'seqspec_of': [sequence_file['@id']]}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        configuration_file_json['@id'],
        {'content_type': 'seqspec',
         'seqspec_of': [sequence_file['@id']]})
    assert res.status_code == 200
