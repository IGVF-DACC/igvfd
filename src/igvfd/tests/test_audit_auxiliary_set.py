import pytest


def test_audit_auxiliary_set_with_non_sequence_files(
    testapp,
    base_auxiliary_set,
    principal_analysis_set,
    reference_file
):
    testapp.patch_json(
        reference_file['@id'],
        {'file_set': base_auxiliary_set['@id']}
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected files'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        reference_file['@id'],
        {'file_set': principal_analysis_set['@id']}
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected files'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_unexpected_virtual_sample(
    testapp,
    base_auxiliary_set,
    in_vitro_cell_line
):
    testapp.patch_json(
        base_auxiliary_set['@id'],
        {
            'samples': [in_vitro_cell_line['@id']]
        }
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected sample'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'virtual': True
        }
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected sample'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_missing_measurement_sets(
    testapp,
    auxiliary_set_cell_sorting,
    measurement_set
):
    res = testapp.get(auxiliary_set_cell_sorting['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing measurement set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'auxiliary_sets': [auxiliary_set_cell_sorting['@id']]
        }
    )
    res = testapp.get(auxiliary_set_cell_sorting['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing measurement set'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_files_associated_with_incorrect_fileset(testapp, base_auxiliary_set, configuration_file_seqspec, sequence_file):
    # Test 1: seqfiles file set != seqspec file set (audit)
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file['@id']],
            'file_set': base_auxiliary_set['@id']
        }
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing related files'
        for error in res.json['audit'].get('ERROR', [])
    )

    # Test 2: seqfiles file set == seqspec file set (no audit)
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': base_auxiliary_set['@id']
        }
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing related files'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_inconsistent_seqspec(testapp, base_auxiliary_set, configuration_file_seqspec, configuration_file_seqspec_2, sequence_file, sequence_file_sequencing_run_2):
    # Test 1: seqfiles from the same set have different seqspecs (audit)
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': base_auxiliary_set['@id'],
            'illumina_read_type': 'R1',
            'sequencing_run': 1,
            'lane': 1
        }
    )
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file['@id']]
        }
    )
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'file_set': base_auxiliary_set['@id'],
            'illumina_read_type': 'R2',
            'sequencing_run': 1,
            'lane': 1
        }
    )
    testapp.patch_json(
        configuration_file_seqspec_2['@id'],
        {
            'seqspec_of': [sequence_file_sequencing_run_2['@id']]
        }
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent sequence specifications'
        for error in res.json['audit'].get('ERROR', [])
    )

    # Test 2: same seqspec linked to different sequence sets (no audit)
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'sequencing_run': 2
        }
    )
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file['@id'], sequence_file_sequencing_run_2['@id']]
        }
    )
    testapp.patch_json(
        configuration_file_seqspec_2['@id'],
        {
            'seqspec_of': [sequence_file['@id'], sequence_file_sequencing_run_2['@id']]
        }
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent sequence specifications'
        for error in res.json['audit'].get('ERROR', [])
    )

    # Test 3: when everything is correct
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'sequencing_run': 1
        }
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent sequence specifications'
        for error in res.json['audit'].get('ERROR', [])
    )
