import pytest


def test_seqspec_of_dependency(testapp, configuration_file_json, sequence_file):
    res = testapp.patch_json(
        configuration_file_json['@id'],
        {'seqspec_of': [sequence_file['@id']]}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        configuration_file_json['@id'],
        {'content_type': 'seqspec',
         'seqspec_of': [sequence_file['@id']],
         'file_format': 'yaml'})
    assert res.status_code == 200


def test_seqspec_file_format_depdendency(testapp, configuration_file_seqspec):
    res = testapp.patch_json(
        configuration_file_seqspec['@id'],
        {'file_format': 'json'}, expect_errors=True)
    assert res.status_code == 422
