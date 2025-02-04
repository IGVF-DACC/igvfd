import pytest


def test_audit_missing_files(
    testapp,
    construct_library_set_reporter,
    reference_file
):
    res = testapp.get(construct_library_set_reporter['@id'] + '@@audit')
    assert res.json.get('files', '') == ''
    assert any(
        error['category'] == 'missing files'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        reference_file['@id'],
        {
            'file_set': construct_library_set_reporter['@id']
        }
    )
    res = testapp.get(construct_library_set_reporter['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing files'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_input_file_set_for(
    testapp,
    measurement_set_mpra,
    analysis_set_base,
    sequence_file
):
    res = testapp.get(measurement_set_mpra['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing analysis'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': measurement_set_mpra['@id']
        }
    )
    res = testapp.get(measurement_set_mpra['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing analysis'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set_mpra['@id']]
        }
    )
    res = testapp.get(measurement_set_mpra['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing analysis'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_inconsistent_location_files(testapp, sequence_file_pod5, sequence_file, measurement_set):
    testapp.patch_json(
        sequence_file['@id'],
        {
            'externally_hosted': True,
            'external_host_url': 'http://test_url',
            'file_set': measurement_set['@id']
        }
    )
    testapp.patch_json(
        sequence_file_pod5['@id'],
        {
            'file_set': measurement_set['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')

    assert any(
        error['category'] == 'inconsistent hosting locations'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        sequence_file_pod5['@id'],
        {
            'externally_hosted': True,
            'external_host_url': 'http://test_url'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')

    assert all(
        error['category'] != 'inconsistent hosting locations'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_single_cell_read_names(testapp, measurement_set_one_onlist, sequence_file, sequence_file_sequencing_run_2):
    # Patch a single cell MeaSet SeqFiles without read_names (audit)
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': measurement_set_one_onlist['@id']
        }
    )
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'file_set': measurement_set_one_onlist['@id']
        }
    )
    res = testapp.get(measurement_set_one_onlist['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing read names'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    # Patch the a MeaSet with one SeqFile with read_names and one without (audit)
    testapp.patch_json(
        sequence_file['@id'],
        {
            'read_names': ['Read 1'],
        }
    )
    res = testapp.get(measurement_set_one_onlist['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing read names'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    # Patch both SeqFiles with read_names (no audit)
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'read_names': ['Read 2', 'Barcode index']
        }
    )
    res = testapp.get(measurement_set_one_onlist['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing read names'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    # Patch a SeqFile with unexpected read_names (audit)
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'read_names': ['UMI', 'Read 2']
        }
    )
    res = testapp.get(measurement_set_one_onlist['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected read names'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
