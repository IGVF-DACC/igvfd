import pytest


def test_seqspec_of_link(testapp, configuration_file_seqspec, sequence_file, sequence_file_sequencing_run_2):
    testapp.patch_json(
        sequence_file['@id'],
        {
            'seqspec': configuration_file_seqspec['@id']
        }
    )
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'seqspec': configuration_file_seqspec['@id']
        }
    )
    res = testapp.get(configuration_file_seqspec['@id'])
    assert set(res.json.get('seqspec_of')) == {sequence_file['@id'], sequence_file_sequencing_run_2['@id']}
