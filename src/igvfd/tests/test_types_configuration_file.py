import pytest


def test_validate_onlist_files(testapp, configuration_file_json, configuration_file_seqspec, sequence_file, measurement_set_one_onlist, base_auxiliary_set, measurement_set_perturb_seq, measurement_set_mpra, assay_term_scrna):
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

    # If a seqspec is seqspec_of to a sequence file in an auxiliary set not associated with any measurement set do not validate onlist
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': base_auxiliary_set['@id']
        }
    )
    res = testapp.get(configuration_file_seqspec['@id'])
    assert res.json.get('validate_onlist_files', '') is False
    # If a seqspec is seqspec_of to a sequence file in an auxiliary set associated with a non-single cell measurement set do not validate onlist
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(configuration_file_seqspec['@id'])
    assert res.json.get('validate_onlist_files', '') is False
    # If a seqspec is seqspec_of to a sequence file in an auxiliary set associated with a single cell (but not Perturb-seq) measurement set do not validate onlist
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'assay_term': assay_term_scrna['@id']
        }
    )
    res = testapp.get(configuration_file_seqspec['@id'])
    assert res.json.get('validate_onlist_files', '') is False
    # If a seqspec is seqspec_of to a sequence file in an auxiliary set associated with a Perturb-seq measurement set validate onlist
    testapp.patch_json(
        measurement_set_perturb_seq['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(configuration_file_seqspec['@id'])
    assert res.json.get('validate_onlist_files', '') is True
