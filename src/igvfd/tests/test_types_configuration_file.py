import pytest


def test_validate_onlist_files(testapp, configuration_file_json, configuration_file_seqspec, sequence_file, measurement_set_one_onlist, base_auxiliary_set, measurement_set_perturb_seq):
    # If a configuration file is NOT a seqspec
    res = testapp.get(configuration_file_json['@id'])
    assert res.json.get('validate_onlist_files', '') is False

    # If a seqpec configuration file has no seqspec_of
    res = testapp.get(configuration_file_seqspec['@id'])
    assert res.json.get('validate_onlist_files', '') is False

    # If a configuration file seqspec is seqspec_of a sequence file in an analysis set
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file['@id']]
        }
    )
    res = testapp.get(configuration_file_seqspec['@id'])
    assert res.json.get('validate_onlist_files', '') is False

    # If a seqspec is seqspec_of to a sequence file in a single cell Measurement Set
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': measurement_set_one_onlist['@id']
        }
    )
    res = testapp.get(configuration_file_seqspec['@id'])
    assert res.json.get('validate_onlist_files', '') is True

    # If a seqspec is seqspec_of to a sequence file in a perturb-seq auxiliary set
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': base_auxiliary_set['@id']
        }
    )
    res = testapp.get(configuration_file_seqspec['@id'])
    assert res.json.get('validate_onlist_files', '') is False
    testapp.patch_json(
        measurement_set_perturb_seq['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(configuration_file_seqspec['@id'])
    assert res.json.get('validate_onlist_files', '') is True
