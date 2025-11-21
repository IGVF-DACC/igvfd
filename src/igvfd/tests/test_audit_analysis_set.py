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
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set['@id']]
            'demultiplexed_samples': [tissue['@id']]
        }
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
            'demultiplexed_samples': [tissue['@id']]
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
            'demultiplexed_samples': [primary_cell['@id']]
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
            'demultiplexed_samples': [tissue['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent demultiplexed sample'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_analysis_set_inconsistent_barcode_onlist(
    testapp,
    analysis_set_with_scrna_measurement_sets,
    analysis_set_with_multiome_measurement_sets,
    measurement_set_one_onlist,
    measurement_set_two_onlists,
    measurement_set_one_onlist_atac,
    measurement_set_two_onlists_atac,
    tabular_file_onlist_1,
    tabular_file_onlist_2,
    signal_file,
    analysis_step_version,
    base_workflow
):
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
    # Each assay type has 2 measurement sets with different onlist info,
    # but workflow is non-uniform: (no audit)
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
    testapp.patch_json(
        signal_file['@id'],
        {
            'file_set': analysis_set_with_multiome_measurement_sets['@id'],
            'analysis_step_version': analysis_step_version['@id']
        }
    )
    res = testapp.get(analysis_set_with_multiome_measurement_sets['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent barcode onlists'
        for error in res.json['audit'].get('WARNING', [])
    )
    assert all(
        error['category'] != 'inconsistent barcode method'
        for error in res.json['audit'].get('WARNING', [])
    )
    # Same as above, but workflow is uniform. (audit)
    testapp.patch_json(
        base_workflow['@id'],
        {
            'uniform_pipeline': True
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


def test_audit_missing_genome_or_transcriptome(
    testapp,
    analysis_set_base,
    alignment_file,
    reference_file,
    reference_file_with_assembly,
    tabular_file_onlist_1,
    tabular_file_bed,
    measurement_set,
    assay_term_bulk_rna,
    assay_term_scatac,
    sequence_file,
    tabular_file
):
    # Overall note: The test spot checks Alignment Files, but the idea is the same for matrix and signal files.
    # Test: If an alignment file is derived from a non-seq file and has genome ref, no audit
    testapp.patch_json(
        alignment_file['@id'],
        {
            'file_set': analysis_set_base['@id'],
            'derived_from': [tabular_file_onlist_1['@id']],
            'reference_files': [reference_file['@id']]
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
    # Test: If an alignment file is derived from a non-transcript seqfile and has genome ref, no audit
    testapp.patch_json(
        alignment_file['@id'],
        {
            'derived_from': [sequence_file['@id']]
        }
    )
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': measurement_set['@id']
        }
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_scatac['@id']
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing reference files'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    # Test: If an alignment file is derived from a transcript seqfile and has genome ref, audit
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_bulk_rna['@id']
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing reference files'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    # Test: If an alignment file is derived from a transcript seqfile and has transcript ref, no audit
    testapp.patch_json(
        reference_file['@id'],
        {
            'content_type': 'transcriptome index'
        }
    )
    testapp.patch_json(
        alignment_file['@id'],
        {
            'reference_files': [reference_file['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing reference files'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    # Test 2 lvls up: If an alignment file is derived from a tab file,
    # which is derived from a transcript seqfile and has transcript ref, no audit
    testapp.patch_json(
        alignment_file['@id'],
        {
            'derived_from': [tabular_file['@id']]
        }
    )
    # SeqFile is linked an RNA measurement set
    testapp.patch_json(
        tabular_file['@id'],
        {
            'derived_from': [sequence_file['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing reference files'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    # Test 2 lvls up: If an alignment file is derived from a tab file,
    # which is derived from a transcript seqfile and has genome ref, audit
    testapp.patch_json(
        reference_file['@id'],
        {
            'content_type': 'genome reference'
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing reference files'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    # A tabular file can trigger the same audit, but in the
    # internal action category.
    testapp.patch_json(
        tabular_file_bed['@id'],
        {
            'file_set': analysis_set_base['@id'],
            'derived_from': [sequence_file['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing reference files'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )


def test_audit_inconsistent_controlled_access_analysis_set(
    testapp,
    principal_analysis_set,
    analysis_set_base,
    controlled_access_alignment_file,
    tissue,
    institutional_certificate
):
    # The Analysis Set has a controlled bam, resulting in the audit.
    testapp.patch_json(
        institutional_certificate['@id'],
        {
            'samples': [tissue['@id']]
        }
    )
    res = testapp.get(principal_analysis_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent controlled access'
        for error in res.json['audit'].get('ERROR', [])
    )
    # Move the controlled file away to a different file set.
    testapp.patch_json(
        controlled_access_alignment_file['@id'],
        {
            'file_set': analysis_set_base['@id']
        }
    )
    res = testapp.get(principal_analysis_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent controlled access'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_multiple_barcode_replacement_files_in_input_anaset(
    testapp,
    analysis_set_base,
    measurement_set,
    measurement_set_multiome,
    tabular_file,
    tabular_file_barcode_replacement
):
    # Test 1: 2 Parse input file sets with 2 barcode replacement file (audit)
    testapp.patch_json(
        measurement_set['@id'],
        {
            'barcode_replacement_file': tabular_file_barcode_replacement['@id'],
            'preferred_assay_titles': ['Parse SPLiT-seq']
        }
    )
    testapp.patch_json(
        tabular_file['@id'],
        {
            'content_type': 'barcode replacement'
        }
    )
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'barcode_replacement_file': tabular_file['@id'],
            'preferred_assay_titles': ['Parse SPLiT-seq']
        }
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets':
                [
                    measurement_set['@id'],
                    measurement_set_multiome['@id']
                ]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected barcode replacement file'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )

    # Test 2: 2 Parse input filesets with 1 barcode replacement file (audit)
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'barcode_replacement_file': tabular_file_barcode_replacement['@id']
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected barcode replacement file'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_missing_pipeline_parameters(
    testapp,
    analysis_set_base,
    tabular_file,
    workflow_uniform_pipeline,
    analysis_step_version,
    document_pipeline_parameters
):
    testapp.patch_json(
        tabular_file['@id'],
        {
            'analysis_step_version': analysis_step_version['@id'],
            'file_set': analysis_set_base['@id']
        }
    )
    testapp.patch_json(
        workflow_uniform_pipeline['@id'],
        {
            'uniform_pipeline': False
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing pipeline parameters'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        workflow_uniform_pipeline['@id'],
        {
            'uniform_pipeline': True
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing pipeline parameters'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'pipeline_parameters': [document_pipeline_parameters['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing pipeline parameters'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_inconsistent_pipeline_parameters(
    testapp,
    analysis_set_base,
    experimental_protocol_document,
    document_pipeline_parameters,
    tabular_file
):
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'pipeline_parameters': [experimental_protocol_document['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent pipeline parameters'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'pipeline_parameters': [document_pipeline_parameters['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent pipeline parameters'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'pipeline_parameters': [document_pipeline_parameters['@id'], tabular_file['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent pipeline parameters'
        for error in res.json['audit'].get('ERROR', [])
    )

    testapp.patch_json(
        tabular_file['@id'],
        {
            'content_type': 'pipeline parameters'
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent pipeline parameters'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_documents(
    testapp,
    analysis_set_base,
    document_pipeline_parameters,
    experimental_protocol_document
):
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'documents': [document_pipeline_parameters['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent documents'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'pipeline_parameters': [document_pipeline_parameters['@id']],
            'documents': [experimental_protocol_document['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent documents'
        for error in res.json['audit'].get('ERROR', [])
    )
