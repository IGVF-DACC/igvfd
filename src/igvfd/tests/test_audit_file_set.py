import pytest


def test_audit_missing_files(
    testapp,
    construct_library_set_reporter,
    measurement_set_no_files,
    reference_file
):
    res = testapp.get(measurement_set_no_files['@id'] + '@@audit')
    assert res.json.get('files', '') == ''
    assert any(
        error['category'] == 'missing files'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        measurement_set_no_files['@id'],
        {
            'preferred_assay_titles': ['Cell painting']
        }
    )
    res = testapp.get(measurement_set_no_files['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing files'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        reference_file['@id'],
        {'file_set': measurement_set_no_files['@id']}
    )
    testapp.patch_json(
        measurement_set_no_files['@id'],
        {'preferred_assay_titles': ['CRISPR FlowFISH screen']}
    )
    res = testapp.get(measurement_set_no_files['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing files'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
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
    principal_analysis_set,
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
    assert any(
        error['category'] == 'missing principal analysis'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        principal_analysis_set['@id'],
        {
            'input_file_sets': [analysis_set_base['@id']]
        }
    )
    res = testapp.get(measurement_set_mpra['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing principal analysis'
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
    # Patch a single cell SeqFiles without read_names and I1 (no audit)
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': measurement_set_one_onlist['@id'],
            'illumina_read_type': 'I1'
        }
    )
    res = testapp.get(measurement_set_one_onlist['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing read names'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    # Patch a single cell SeqFiles without read_names and R1 (audit)
    testapp.patch_json(
        sequence_file['@id'],
        {
            'illumina_read_type': 'R1'
        }
    )
    res = testapp.get(measurement_set_one_onlist['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing read names'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    # Patch SeqFiles with R-read type and read_names (no audit)
    testapp.patch_json(
        sequence_file['@id'],
        {
            'read_names': ['Read 1']
        }
    )
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'file_set': measurement_set_one_onlist['@id'],
            'illumina_read_type': 'R2',
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


def test_audit_control_for_control_type(
    testapp,
    measurement_set_mpra,
    construct_library_set_reporter,
    analysis_set_base
):
    res = testapp.get(measurement_set_mpra['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing control for'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    assert all(
        error['category'] != 'missing control type'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        construct_library_set_reporter['@id'],
        {
            'control_file_sets': [measurement_set_mpra['@id']]
        }
    )
    res = testapp.get(measurement_set_mpra['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing control type'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'control_types': ['low FACS signal']
        }
    )
    res = testapp.get(measurement_set_mpra['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing control type'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    assert all(
        error['category'] != 'missing control for'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        construct_library_set_reporter['@id'],
        {
            'control_file_sets': [analysis_set_base['@id']]
        }
    )
    res = testapp.get(measurement_set_mpra['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing control for'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_missing_publication(
    testapp,
    measurement_set_no_files,
    publication,
    curated_set_genome
):
    res = testapp.get(measurement_set_no_files['@id'] + '@@audit')
    assert res.json.get('publications', '') == ''
    testapp.patch_json(
        measurement_set_no_files['@id'],
        {
            'status': 'released',
            'release_timestamp': '2025-03-06T12:34:56Z'
        }
    )
    res = testapp.get(measurement_set_no_files['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing publication'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )
    testapp.patch_json(
        measurement_set_no_files['@id'],
        {
            'publications': [publication['@id']]
        }
    )
    res = testapp.get(measurement_set_no_files['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing publication'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )
    # Curated sets are not expected to link to publications.
    testapp.patch_json(
        curated_set_genome['@id'],
        {
            'status': 'released',
            'release_timestamp': '2025-10-06T12:34:56Z'
        }
    )
    res = testapp.get(curated_set_genome['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing publication'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )


def test_audit_missing_description(
    testapp,
    analysis_set_base,
    measurement_set_no_files
):
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing description'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'file_set_type': 'principal analysis',
            'input_file_sets': [measurement_set_no_files['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing description'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'description': 'Description of experiment.'
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing description'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
