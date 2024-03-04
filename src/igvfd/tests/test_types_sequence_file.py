import pytest


def test_seqspec_link(testapp, configuration_file_seqspec, configuration_file_seqspec_2, sequence_file):
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file['@id']]
        }
    )
    testapp.patch_json(
        configuration_file_seqspec_2['@id'],
        {
            'seqspec_of': [sequence_file['@id']]
        }
    )
    res = testapp.get(sequence_file['@id'])
    assert set(res.json.get('seqspec')) == {configuration_file_seqspec['@id'], configuration_file_seqspec_2['@id']}
