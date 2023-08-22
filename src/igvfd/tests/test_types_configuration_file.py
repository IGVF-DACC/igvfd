import pytest


def test_seqspec_for_link(testapp, configuration_file_seqspec, sequence_file, sequence_file_s3_uri):
    testapp.patch_json(
        sequence_file['@id'],
        {
            'seqspec': [configuration_file_seqspec['@id']]
        }
    )
    testapp.patch_json(
        sequence_file_s3_uri['@id'],
        {
            'seqspec': [configuration_file_seqspec['@id']]
        }
    )
    res = testapp.get(configuration_file_seqspec['@id'])
    assert set([file_id['@id'] for file_id in res.json.get('seqspec_for')]
               ) == {sequence_file['@id'], sequence_file_s3_uri['@id']}
