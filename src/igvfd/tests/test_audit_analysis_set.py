import pytest


def test_audit_missing_input_file_set(
    testapp,
    analysis_set_base,
    measurement_set,
    matrix_file,
    signal_file
):
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing input file set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        signal_file['@id'],
        {
            'file_set': measurement_set['@id']
        }
    )
    testapp.patch_json(
        matrix_file['@id'],
        {
            'file_set': analysis_set_base['@id'],
            'derived_from': [signal_file['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing input file set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        signal_file['@id'],
        {
            'file_set': analysis_set_base['@id']
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing input file set'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_missing_derived_from(
    testapp,
    analysis_set_base,
    matrix_file,
    signal_file
):
    testapp.patch_json(
        matrix_file['@id'],
        {
            'file_set': analysis_set_base['@id']
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing derived from'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        matrix_file['@id'],
        {
            'derived_from': [signal_file['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing derived from'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_unexpected_input_file_set(
    testapp,
    analysis_set_base,
    matrix_file,
    signal_file,
    measurement_set_multiome
):
    testapp.patch_json(
        matrix_file['@id'],
        {
            'file_set': analysis_set_base['@id']
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set_multiome['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected input file set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        matrix_file['@id'],
        {
            'derived_from': [signal_file['@id']]
        }
    )
    testapp.patch_json(
        signal_file['@id'],
        {
            'file_set': measurement_set_multiome['@id']
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected input file set'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_missing_analysis_step_version(
    testapp,
    intermediate_analysis_set,
    matrix_file,
    analysis_step_version
):
    testapp.patch_json(
        matrix_file['@id'],
        {
            'file_set': intermediate_analysis_set['@id']
        }
    )
    res = testapp.get(intermediate_analysis_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing analysis step version'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        matrix_file['@id'],
        {
            'analysis_step_version': analysis_step_version['@id']
        }
    )
    res = testapp.get(intermediate_analysis_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing analysis step version'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_multiple_workflows(
    testapp,
    analysis_set_with_workflow,
    matrix_file_with_base_workflow,
    matrix_file_with_base_workflow_2
):
    # Test when an analysis set only has one workflow
    res = testapp.get(analysis_set_with_workflow['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected workflows'
        for error in res.json['audit'].get('WARNING', [])
    )
    # Patching 2 matrix files to a single analysis set
    # Two workflows for a single analysis set
    testapp.patch_json(
        matrix_file_with_base_workflow['@id'],
        {
            'file_set': analysis_set_with_workflow['@id']
        }
    )
    testapp.patch_json(
        matrix_file_with_base_workflow_2['@id'],
        {
            'file_set': analysis_set_with_workflow['@id']
        }
    )
    res = testapp.get(analysis_set_with_workflow['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected workflows'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_analysis_set_multiplexed_samples(
    testapp,
    analysis_set_base,
    measurement_set,
    measurement_set_no_files,
    in_vitro_differentiated_cell,
    tissue,
    multiplexed_sample,
    analysis_set_no_input
):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [multiplexed_sample['@id']]
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing demultiplexed sample'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'demultiplexed_sample': tissue['@id']
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing demultiplexed sample'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [in_vitro_differentiated_cell['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected demultiplexed sample'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        measurement_set_no_files['@id'],
        {
            'samples': [multiplexed_sample['@id']]
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set['@id'], measurement_set_no_files['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected samples'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        analysis_set_no_input['@id'],
        {
            'demultiplexed_sample': tissue['@id']
        }
    )
    res = testapp.get(analysis_set_no_input['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected demultiplexed sample'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_analysis_set_demultiplexed_sample(
    testapp,
    analysis_set_base,
    measurement_set,
    in_vitro_differentiated_cell,
    tissue,
    primary_cell,
    multiplexed_sample
):
    testapp.patch_json(
        multiplexed_sample['@id'],
        {
            'multiplexed_samples': [tissue['@id'], in_vitro_differentiated_cell['@id']]
        }
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [multiplexed_sample['@id']]
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set['@id']],
            'demultiplexed_sample': primary_cell['@id']
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent demultiplexed sample'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'demultiplexed_sample': tissue['@id']
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent demultiplexed sample'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_analysis_set_inconsistent_barcode_onlist(testapp, analysis_set_with_scrna_measurement_sets, analysis_set_with_multiome_measurement_sets, measurement_set_one_onlist, measurement_set_two_onlists, measurement_set_one_onlist_atac, measurement_set_two_onlists_atac, tabular_file_onlist_1, tabular_file_onlist_2):
    # Analysis set with 1 ATAC measurement set and 1 RNA measurement set with different onlist info (no audit)
    res = testapp.get(analysis_set_with_multiome_measurement_sets['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent barcode onlists'
        for error in res.json['audit'].get('WARNING', [])
    )
    assert all(
        error['category'] != 'inconsistent barcode method'
        for error in res.json['audit'].get('WARNING', [])
    )

    # Analysis set with 2 ATAC measurement set and 2 RNA measurement set
    # Each assay type has 2 measurement sets with different onlist info (audit)
    testapp.patch_json(
        analysis_set_with_multiome_measurement_sets['@id'],
        {
            'input_file_sets': [measurement_set_one_onlist['@id'],
                                measurement_set_two_onlists['@id'],
                                measurement_set_one_onlist_atac['@id'],
                                measurement_set_two_onlists_atac['@id']
                                ]
        }
    )
    res = testapp.get(analysis_set_with_multiome_measurement_sets['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent barcode onlists'
        for error in res.json['audit'].get('WARNING', [])
    )
    assert any(
        error['category'] == 'inconsistent barcode method'
        for error in res.json['audit'].get('WARNING', [])
    )

    # Patch the single onlist file measurement sets to be 2 onlist files and product as method (no audit)
    testapp.patch_json(
        measurement_set_one_onlist['@id'],
        {
            'onlist_files': [tabular_file_onlist_1['@id'], tabular_file_onlist_2['@id']],
            'onlist_method': 'product'
        }
    )
    testapp.patch_json(
        measurement_set_one_onlist_atac['@id'],
        {
            'onlist_files': [tabular_file_onlist_1['@id'], tabular_file_onlist_2['@id']],
            'onlist_method': 'product'
        }
    )
    res = testapp.get(analysis_set_with_scrna_measurement_sets['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent barcode onlists'
        for error in res.json['audit'].get('WARNING', [])
    )
    assert all(
        error['category'] != 'inconsistent barcode method'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_missing_transcriptome(
    testapp,
    analysis_set_base,
    alignment_file,
    reference_file,
    measurement_set,
    assay_term_bulk_rna
):
    testapp.patch_json(
        alignment_file['@id'],
        {
            'file_set': analysis_set_base['@id']
        }
    )
    testapp.patch_json(
        reference_file['@id'],
        {
            'content_type': 'genome reference'
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing reference files'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_bulk_rna['@id']
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing reference files'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        reference_file['@id'],
        {
            'content_type': 'transcriptome reference'
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing reference files'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
