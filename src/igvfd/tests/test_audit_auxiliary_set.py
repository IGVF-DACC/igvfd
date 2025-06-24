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


def test_audit_files_associated_with_incorrect_fileset_auxset(testapp, base_auxiliary_set, configuration_file_seqspec, sequence_file):
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


def test_audit_inconsistent_seqspec_auxset(testapp, base_auxiliary_set, configuration_file_seqspec, configuration_file_seqspec_2, sequence_file, sequence_file_sequencing_run_2):
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


def test_audit_unexpected_seqspec_auxset(testapp, sequence_file_pod5, sequence_file, sequence_file_sequencing_run_2, configuration_file_seqspec, base_auxiliary_set, auxiliary_set_cell_sorting, experimental_protocol_document):
    # Test: If pod5, seqspec is unexpected (audit)
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file_pod5['@id']],
            'file_set': base_auxiliary_set['@id']
        }
    )
    testapp.patch_json(
        sequence_file_pod5['@id'],
        {
            'file_set': base_auxiliary_set['@id']
        }
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected sequence specification'
        for error in res.json['audit'].get('ERROR', [])
    )
    # Patch: make a seqspec document
    testapp.patch_json(
        experimental_protocol_document['@id'],
        {
            'document_type': 'library structure seqspec',
        }
    )
    # Test: If double seqspec and non-single cell (audit)
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file['@id']],
            'file_set': auxiliary_set_cell_sorting['@id']
        }
    )
    testapp.patch_json(
        sequence_file['@id'],
        {
            'seqspec_document': experimental_protocol_document['@id'],
            'file_set': auxiliary_set_cell_sorting['@id']
        }
    )
    res = testapp.get(auxiliary_set_cell_sorting['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected sequence specification'
        for error in res.json['audit'].get('ERROR', [])
    )
    # Test: If wrong seqspec document type (audit)
    testapp.patch_json(
        experimental_protocol_document['@id'],
        {
            'document_type': 'standards',
        }
    )
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'seqspec_document': experimental_protocol_document['@id'],
            'file_set': auxiliary_set_cell_sorting['@id']
        }
    )
    res = testapp.get(auxiliary_set_cell_sorting['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected sequence specification'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_missing_seqspec_auxset(testapp, sequence_file, sequence_file_sequencing_run_2, experimental_protocol_document, configuration_file_seqspec, base_auxiliary_set):
    # Patch: make a seqspec document
    testapp.patch_json(
        experimental_protocol_document['@id'],
        {
            'document_type': 'library structure seqspec',
        }
    )
    # Test 1: SeqFiles without seqspec config or doc (Internal action)
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': base_auxiliary_set['@id']
        }
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing sequence specification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )

    # Test 2: SeqFile with seqspec doc (no internal action)
    testapp.patch_json(
        sequence_file['@id'],
        {
            'seqspec_document': experimental_protocol_document['@id']
        }
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing sequence specification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )

    # Test 3: SeqFile with seqspec ConfigFile (no internal action)
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'file_set': base_auxiliary_set['@id']
        }
    )
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'file_set': base_auxiliary_set['@id'],
            'seqspec_of': [sequence_file_sequencing_run_2['@id']]
        }
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing sequence specification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_missing_barcode_map(
    testapp,
    auxiliary_set_cell_hashing,
    tabular_file
):
    res = testapp.get(auxiliary_set_cell_hashing['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing barcode map'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        auxiliary_set_cell_hashing['@id'],
        {
            'barcode_map': tabular_file['@id']
        }
    )
    res = testapp.get(auxiliary_set_cell_hashing['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent barcode map'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        tabular_file['@id'],
        {
            'content_type': 'barcode to hashtag mapping'
        }
    )
    res = testapp.get(auxiliary_set_cell_hashing['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing barcode map'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    assert all(
        error['category'] != 'inconsistent barcode map'
        for error in res.json['audit'].get('ERROR', [])
    )
