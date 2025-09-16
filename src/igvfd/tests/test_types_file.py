import pytest

from igvfd.types.file import File


def test_types_file_get_external_sheet(sequence_file, root):
    item = root.get_by_uuid(
        sequence_file['uuid']
    )
    actual = item._get_external_sheet()
    expected = {
        'key': '2023/01/21/8513c860-0e63-4e95-9459-f17a8f6ad45d/IGVFFF598NQZ.fastq.gz',
        'bucket': 'igvf-files-local',
        'service': 's3',
        'upload_credentials': {
            'access_key': 'AKIAIOSFODNN7EXAMPLE',
            'expiration': '2023-01-22T12:52:06.074000+00:00',
            'request_id': 'W36V9TIIUQGMWOX46LZHLLHDTG8U6HAONL18PGZLFOVLH5EQDEDO',
            'secret_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYzEXAMPLEKEY',
            'upload_url': 's3://igvf-files-local/2023/01/21/8513c860-0e63-4e95-9459-f17a8f6ad45d/IGVFFF598NQZ.fastq.gz',
            'session_token': 'AQoDYXdzEPT//////////wEXAMPLEtc764bNrC9SAPBSM22wDOk4x4HIZ8j4FZTwdQWLWsKWHGBuFqwAeMicRXmxfpSPfIeoIYRqTflfKD8YUuwthAx7mSEI/qkPpKPi/kMcGdQrmGdeehM4IC1NtBmUpp2wUE8phUZampKsburEDy0KPkyQDYwT7WZ0wq5VSXDvp75YU9HFvlRd8Tx6q6fE8YQcHNVXAkiY9q6d+xo0rKwT38xVqr7ZD0u0iPPkUL64lIZbqBAz+scqKmlzm8FDrypNC9Yjc8fPOLn9FX9KSYvKTr4rvx3iSIlTJabIQwj2ICCR/oLxBA==',
            'federated_user_id': '000000000000:up1674262326.067452-IGVFFF598NQZ',
            'federated_user_arn': 'arn:aws:sts::000000000000:federated-user/up1674262326.067452-IGVFFF598NQZ'
        }
    }
    for key in ['key', 'bucket', 'service', 'upload_credentials']:
        assert key in actual
    for key in expected['upload_credentials']:
        assert key in actual['upload_credentials']
    for key in ['bucket', 'service']:
        assert actual[key] == expected[key]


def test_types_file_set_external_sheet(sequence_file, root):
    item = root.get_by_uuid(
        sequence_file['uuid']
    )
    external_to_set = {'bucket': 'new_test_file_bucket', 'key': 'abc.bam'}
    item._set_external_sheet(
        external_to_set
    )
    actual = item._get_external_sheet()
    expected = {
        'key': 'abc.bam',
        'bucket': 'new_test_file_bucket',
        'service': 's3',
    }
    for k, v in expected.items():
        assert actual[k] == v


def test_types_file_s3_uri_is_present(sequence_file):
    assert 's3_uri' in sequence_file


def test_types_file_s3_creation_when_externally_hosted(externally_hosted_sequence_file):
    assert 's3_uri' not in externally_hosted_sequence_file
    assert 'href' not in externally_hosted_sequence_file
    assert externally_hosted_sequence_file['upload_status'] == 'validation exempted'


def test_types_file_s3_uri_non_submittable(testapp, principal_analysis_set, award, lab):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '515c8a6af303ea86bc59c629ff198277',
        'file_format': 'fastq',
        'file_set': principal_analysis_set['@id'],
        'minimum_read_length': 99,
        'maximum_read_length': 101,
        'mean_read_length': 100,
        'read_count': 23040138,
        'file_size': 5495803,
        'content_type': 'reads',
        'sequencing_run': 1,
        's3_uri': 's3://foo/bar/baz.fastq.gz'
    }
    testapp.post_json('/sequence_file/', item, status=422)


def test_types_aligment_file_content_summary(testapp, alignment_file):
    res = testapp.get(alignment_file['@id'])
    assert res.json.get('content_summary') == 'unfiltered alignments'
    testapp.patch_json(
        alignment_file['@id'],
        {
            'redacted': True,
            'filtered': True
        }
    )
    res = testapp.get(alignment_file['@id'])
    assert res.json.get('content_summary') == 'filtered redacted alignments'


def test_types_signal_file_content_summary(testapp, signal_file):
    res = testapp.get(signal_file['@id'])
    assert res.json.get('content_summary') == 'plus strand signal of all reads'
    testapp.patch_json(
        signal_file['@id'],
        {
            'filtered': True,
            'normalized': True,
            'strand_specificity': 'unstranded'
        }
    )
    res = testapp.get(signal_file['@id'])
    assert res.json.get('content_summary') == 'filtered normalized unstranded signal of all reads'


def test_types_matrix_file_content_summary(testapp, matrix_file):
    res = testapp.get(matrix_file['@id'])
    assert res.json.get('content_summary') == 'cell by gene in sparse gene count matrix'
    testapp.patch_json(
        matrix_file['@id'],
        {
            'principal_dimension': 'variant',
            'secondary_dimensions': ['treatment', 'antibody capture'],
            'content_type': 'transcriptome annotations'
        }
    )
    res = testapp.get(matrix_file['@id'])
    assert res.json.get('content_summary') == 'variant by treatment by antibody capture in transcriptome annotations'


def test_types_file_calculated_transcriptome_annotation(testapp, matrix_file, signal_file, alignment_file, reference_file, reference_file_with_transcriptome):
    res = testapp.get(matrix_file['@id'])
    assert res.json.get('transcriptome_annotation') == None
    testapp.patch_json(
        matrix_file['@id'],
        {
            'reference_files': [reference_file_with_transcriptome['@id']]
        }
    )
    res = testapp.get(matrix_file['@id'])
    assert res.json.get('transcriptome_annotation') == 'GENCODE 43'
    testapp.patch_json(
        matrix_file['@id'],
        {
            'reference_files': [reference_file['@id'], reference_file_with_transcriptome['@id']]
        }
    )
    res = testapp.get(matrix_file['@id'])
    assert res.json.get('transcriptome_annotation') == 'Mixed transcriptome annotations'

    # Signal file
    res = testapp.get(signal_file['@id'])
    assert res.json.get('transcriptome_annotation') == None
    testapp.patch_json(
        signal_file['@id'],
        {
            'reference_files': [reference_file_with_transcriptome['@id']]
        }
    )
    res = testapp.get(signal_file['@id'])
    assert res.json.get('transcriptome_annotation') == 'GENCODE 43'
    testapp.patch_json(
        signal_file['@id'],
        {
            'reference_files': [reference_file['@id'], reference_file_with_transcriptome['@id']]
        }
    )
    res = testapp.get(signal_file['@id'])
    assert res.json.get('transcriptome_annotation') == 'Mixed transcriptome annotations'

    # Alignment file
    res = testapp.get(alignment_file['@id'])
    assert res.json.get('transcriptome_annotation') == None
    testapp.patch_json(
        alignment_file['@id'],
        {
            'reference_files': [reference_file_with_transcriptome['@id']]
        }
    )
    res = testapp.get(alignment_file['@id'])
    assert res.json.get('transcriptome_annotation') == 'GENCODE 43'
    testapp.patch_json(
        alignment_file['@id'],
        {
            'reference_files': [reference_file['@id'], reference_file_with_transcriptome['@id']]
        }
    )
    res = testapp.get(alignment_file['@id'])
    assert res.json.get('transcriptome_annotation') == 'Mixed transcriptome annotations'


def test_types_file_calculated_assembly(testapp, matrix_file, signal_file, alignment_file, reference_file, reference_file_with_assembly):
    testapp.patch_json(
        reference_file['@id'],
        {
            'content_type': 'genome reference'
        }
    )
    res = testapp.get(matrix_file['@id'])
    assert res.json.get('assembly') == None
    testapp.patch_json(
        matrix_file['@id'],
        {
            'reference_files': [reference_file_with_assembly['@id']]
        }
    )
    res = testapp.get(matrix_file['@id'])
    assert res.json.get('assembly') == 'GRCh38'
    testapp.patch_json(
        matrix_file['@id'],
        {
            'reference_files': [reference_file['@id'], reference_file_with_assembly['@id']]
        }
    )
    res = testapp.get(matrix_file['@id'])
    assert res.json.get('assembly') == 'Mixed genome assemblies'

    # Signal file
    res = testapp.get(signal_file['@id'])
    assert res.json.get('assembly') == None
    testapp.patch_json(
        signal_file['@id'],
        {
            'reference_files': [reference_file_with_assembly['@id']]
        }
    )
    res = testapp.get(signal_file['@id'])
    assert res.json.get('assembly') == 'GRCh38'
    testapp.patch_json(
        signal_file['@id'],
        {
            'reference_files': [reference_file['@id'], reference_file_with_assembly['@id']]
        }
    )
    res = testapp.get(signal_file['@id'])
    assert res.json.get('assembly') == 'Mixed genome assemblies'

    # Alignment file
    res = testapp.get(alignment_file['@id'])
    assert res.json.get('assembly') == None
    testapp.patch_json(
        alignment_file['@id'],
        {
            'reference_files': [reference_file_with_assembly['@id']]
        }
    )
    res = testapp.get(alignment_file['@id'])
    assert res.json.get('assembly') == 'GRCh38'
    testapp.patch_json(
        alignment_file['@id'],
        {
            'reference_files': [reference_file['@id'], reference_file_with_assembly['@id']]
        }
    )
    res = testapp.get(alignment_file['@id'])
    assert res.json.get('assembly') == 'Mixed genome assemblies'


def test_integrated_in(testapp, construct_library_set_genome_wide, base_expression_construct_library_set, tabular_file):
    testapp.patch_json(
        construct_library_set_genome_wide['@id'],
        {
            'integrated_content_files': [tabular_file['@id']]
        }
    )
    testapp.patch_json(
        base_expression_construct_library_set['@id'],
        {
            'integrated_content_files': [tabular_file['@id']]
        }
    )
    res = testapp.get(tabular_file['@id'])
    assert set([file_set.get('@id') for file_set in res.json.get('integrated_in')]) == {
        base_expression_construct_library_set['@id'], construct_library_set_genome_wide['@id']}


def test_types_controlled_access_uses_restricted_bucket(testapp, controlled_access_alignment_file, alignment_file):
    assert controlled_access_alignment_file['s3_uri'].startswith('s3://igvf-restricted-files-local')
    assert controlled_access_alignment_file['upload_credentials']['upload_url'].startswith(
        's3://igvf-restricted-files-local')
    assert alignment_file['s3_uri'].startswith('s3://igvf-files-local')
    assert alignment_file['upload_credentials']['upload_url'].startswith('s3://igvf-files-local')


def test_types_controlled_access_upload_and_download_bucket_validation(testapp, controlled_access_alignment_file, alignment_file):
    # Assert upload/download works for non controlled-access file.
    res = testapp.get(alignment_file['@id'] + '@@upload')
    assert 'upload_credentials' in res.json['@graph'][0]
    testapp.post_json(alignment_file['@id'] + '@@upload', {}, status=200)
    testapp.get(alignment_file['@id'] + '@@download', status=307)
    # Assert upload/download works for controlled-access file.
    res = testapp.get(controlled_access_alignment_file['@id'] + '@@upload')
    assert 'upload_credentials' in res.json['@graph'][0]
    testapp.post_json(controlled_access_alignment_file['@id'] + '@@upload', {}, status=200)
    testapp.get(controlled_access_alignment_file['@id'] + '@@download', status=307)


def test_types_file_no_download_controlled_access_with_anvil_url(testapp, controlled_access_alignment_file, alignment_file):
    res = testapp.get(alignment_file['@id'])
    assert res.json['controlled_access'] is False
    assert 's3_uri' in res.json
    assert 'href' in res.json
    assert 'anvil_url' not in res.json
    res = testapp.get(controlled_access_alignment_file['@id'])
    assert res.json['controlled_access'] is True
    assert res.json['status'] == 'in progress'
    assert 's3_uri' in res.json
    assert 'href' in res.json
    assert 'anvil_url' not in res.json
    testapp.get(controlled_access_alignment_file['@id'] + '@@upload', status=200)
    testapp.post_json(controlled_access_alignment_file['@id'] + '@@upload', {}, status=200)
    testapp.get(controlled_access_alignment_file['@id'] + '@@download', status=307)
    testapp.patch_json(
        controlled_access_alignment_file['@id'],
        {
            'status': 'released',
            'release_timestamp':  '2024-03-06T12:34:56Z',
            'upload_status': 'validated',
        },
        status=200
    )
    testapp.patch_json(
        controlled_access_alignment_file['@id'],
        {
            'status': 'released',
            'release_timestamp':  '2024-03-06T12:34:56Z',
            'upload_status': 'validated',
            'anvil_url': 'https://abc.123',
        },
        status=200
    )
    res = testapp.get(controlled_access_alignment_file['@id'])
    assert res.json['controlled_access'] is True
    assert res.json['status'] == 'released'
    assert 's3_uri' in res.json
    assert 'href' in res.json
    assert 'anvil_url' in res.json
    testapp.get(controlled_access_alignment_file['@id'] + '@@download', status=307)


def test_input_file_for(testapp, sequence_file_v12, tabular_file_v10):
    testapp.patch_json(
        tabular_file_v10['@id'],
        {
            'derived_from': [sequence_file_v12['@id']]
        }
    )
    res = testapp.get(sequence_file_v12['@id'])
    assert res.json.get('input_file_for', []) == [tabular_file_v10['@id']]


def test_file_summaries(
    testapp,
    alignment_file,
    configuration_file_seqspec,
    configuration_file_json,
    image_file,
    matrix_file,
    model_file,
    reference_file,
    sequence_file,
    sequence_file_pod5,
    signal_file,
    tabular_file,
    base_prediction_set,
    analysis_step_version
):
    # Reference File
    testapp.patch_json(
        reference_file['@id'],
        {
            'assembly': 'custom'
        }
    )
    res = testapp.get(reference_file['@id'])
    assert res.json.get('summary', '') == 'custom assembly transcriptome reference'
    testapp.patch_json(
        reference_file['@id'],
        {
            'assembly': 'GRCh38',
            'transcriptome_annotation': 'GENCODE 43'
        }
    )
    res = testapp.get(reference_file['@id'])
    assert res.json.get('summary', '') == 'GRCh38 GENCODE 43 transcriptome reference'

    # Alignment File
    testapp.patch_json(
        alignment_file['@id'],
        {
            'redacted': True
        }
    )
    res = testapp.get(alignment_file['@id'])
    assert res.json.get('summary', '') == 'GENCODE 43 unfiltered redacted alignments'
    testapp.patch_json(
        alignment_file['@id'],
        {
            'base_modifications': ['5mC', '6mA'],
            'content_type': 'alignments with modifications'
        }
    )
    res = testapp.get(alignment_file['@id'])
    assert res.json.get(
        'summary', '') == 'GENCODE 43 unfiltered redacted alignments with modifications detecting 5mC, 6mA'

    # Image File
    res = testapp.get(image_file['@id'])
    assert res.json.get('summary', '') == 'detected tissue'

    # Matrix File
    res = testapp.get(matrix_file['@id'])
    assert res.json.get('summary', '') == 'cell by gene in sparse gene count matrix'

    # Predictive matrix file with software.
    testapp.patch_json(
        matrix_file['@id'],
        {
            'file_set': base_prediction_set['@id'],
            'filtered': False,
            'analysis_step_version': analysis_step_version['@id']
        }
    )
    res = testapp.get(matrix_file['@id'])
    assert res.json.get(
        'summary', '') == 'predictive unfiltered cell by gene in sparse gene count matrix (Bowtie2 v2.4.4)'

    # Model File
    res = testapp.get(model_file['@id'])
    assert res.json.get('summary', '') == 'graph structure'

    # Sequence File
    testapp.patch_json(
        sequence_file['@id'],
        {
            'illumina_read_type': 'R2'
        }
    )
    res_sequence_file = testapp.get(sequence_file['@id'])
    assert res_sequence_file.json.get('summary', '') == 'R2 reads from sequencing run 1'
    testapp.patch_json(
        sequence_file_pod5['@id'],
        {
            'base_modifications': ['inosine', 'm5C']
        }
    )
    res_sequence_file_pod5 = testapp.get(sequence_file_pod5['@id'])
    assert res_sequence_file_pod5.json.get(
        'summary', '') == 'Nanopore reads detecting inosine, m5C from sequencing run 10'

    # Configuration File
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file['@id']]
        }
    )
    res = testapp.get(configuration_file_seqspec['@id'])
    assert res.json.get('summary', '') == f'seqspec of {res_sequence_file.json.get("accession")}'

    # Predictive configuration file (not seqspec)
    testapp.patch_json(
        configuration_file_json['@id'],
        {
            'file_set': base_prediction_set['@id'],
            'analysis_step_version': analysis_step_version['@id']
        }
    )
    res = testapp.get(configuration_file_json['@id'])
    assert res.json.get('summary', '') == f'predictive scale factors (Bowtie2 v2.4.4)'

    # Signal File
    testapp.patch_json(
        signal_file['@id'],
        {
            'normalized': True,
            'filtered': True
        }
    )
    res = testapp.get(signal_file['@id'])
    assert res.json.get('summary', '') == 'GENCODE 43 filtered normalized plus strand signal of all reads'
    # Predictive signal file with software.
    testapp.patch_json(
        signal_file['@id'],
        {
            'file_set': base_prediction_set['@id'],
            'analysis_step_version': analysis_step_version['@id']
        }
    )
    res = testapp.get(signal_file['@id'])
    assert res.json.get(
        'summary', '') == 'GENCODE 43 predictive filtered normalized plus strand signal of all reads (Bowtie2 v2.4.4)'

    # Tabular File
    testapp.patch_json(
        tabular_file['@id'],
        {
            'assembly': 'GRCh38',
            'transcriptome_annotation': 'GENCODE 43'
        }
    )
    res = testapp.get(tabular_file['@id'])
    assert res.json.get('summary', '') == 'GRCh38 GENCODE 43 peaks'
    testapp.patch_json(
        tabular_file['@id'],
        {
            'file_set': base_prediction_set['@id'],
            'filtered': True
        }
    )
    res = testapp.get(tabular_file['@id'])
    assert res.json.get('summary', '') == 'GRCh38 GENCODE 43 predictive filtered peaks'
    # Predictive tabular file with software.
    testapp.patch_json(
        tabular_file['@id'],
        {
            'analysis_step_version': analysis_step_version['@id']
        }
    )
    res = testapp.get(tabular_file['@id'])
    assert res.json.get('summary', '') == 'GRCh38 GENCODE 43 predictive filtered peaks (Bowtie2 v2.4.4)'
    testapp.patch_json(
        tabular_file['@id'],
        {
            'base_modifications': ['Nm'],
            'content_type': 'plus strand modification state'
        }
    )
    res = testapp.get(tabular_file['@id'])
    assert res.json.get(
        'summary', '') == 'GRCh38 GENCODE 43 predictive filtered plus strand modification state detecting Nm (Bowtie2 v2.4.4)'


def test_barcode_map_for(testapp, multiplexed_sample_v7, tabular_file_v10):
    testapp.patch_json(
        multiplexed_sample_v7['@id'],
        {
            'barcode_map': tabular_file_v10['@id']
        }
    )
    res = testapp.get(tabular_file_v10['@id'])
    assert res.json.get('barcode_map_for', '') == [multiplexed_sample_v7['@id']]


def test_file_assay_titles(
    testapp,
    alignment_file,
    measurement_set_no_files,
    measurement_set_multiome,
    analysis_set_base,
    base_auxiliary_set
):
    testapp.patch_json(
        alignment_file['@id'],
        {
            'file_set': measurement_set_no_files['@id']
        }
    )
    res = testapp.get(alignment_file['@id'])
    assert set(res.json.get('assay_titles', [])) == {'example-tn-1'}
    assert set(res.json.get('preferred_assay_titles', [])) == {'CRISPR FlowFISH screen'}
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set_no_files['@id'], measurement_set_multiome['@id']]
        }
    )
    testapp.patch_json(
        alignment_file['@id'],
        {
            'file_set': analysis_set_base['@id']
        }
    )
    res = testapp.get(alignment_file['@id'])
    assert set(res.json.get('assay_titles', [])) == {'example-tn-1', 'ATAC-seq'}
    assert set(res.json.get('preferred_assay_titles', [])) == {'CRISPR FlowFISH screen', '10x multiome'}
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']],
            'preferred_assay_titles': ['10x multiome with MULTI-seq']
        }
    )
    testapp.patch_json(
        alignment_file['@id'],
        {
            'file_set': base_auxiliary_set['@id']
        }
    )
    res = testapp.get(alignment_file['@id'])
    assert set(res.json.get('assay_titles', [])) == {'ATAC-seq'}
    assert set(res.json.get('preferred_assay_titles', [])) == {'10x multiome with MULTI-seq'}


def test_types_file_file_workflows(
    testapp,
    tabular_file,
    analysis_step_version,
    base_workflow
):
    testapp.patch_json(
        tabular_file['@id'],
        {
            'analysis_step_version': analysis_step_version['@id']
        }
    )
    res = testapp.get(tabular_file['@id'])
    assert [x['@id'] for x in res.json.get('workflows')] == [base_workflow['@id']]


def test_upload_credentials_forbidden_when_upload_status_is_validated(testapp, reference_file):
    testapp.patch_json(
        reference_file['@id'],
        {
            'status': 'in progress',
            'upload_status': 'pending',
            'file_size': 123,
        },
        status=200
    )
    testapp.post_json(reference_file['@id'] + '@@upload', {}, status=200)
    testapp.patch_json(
        reference_file['@id'],
        {
            'status': 'in progress',
            'upload_status': 'validated',
            'file_size': 123,
        },
        status=200)
    testapp.post_json(reference_file['@id'] + '@@upload', {}, status=403)


def test_upload_credentials_forbidden_when_status_is_not_in_progress_or_preview(testapp, reference_file):
    testapp.patch_json(
        reference_file['@id'],
        {
            'status': 'in progress',
            'upload_status': 'invalidated',
            'file_size': 123,
        },
        status=200
    )
    testapp.post_json(reference_file['@id'] + '@@upload', {}, status=200)
    testapp.patch_json(
        reference_file['@id'],
        {
            'status': 'released',
            'upload_status': 'invalidated',
            'file_size': 123,
            'release_timestamp': '2024-03-06T12:34:56Z',
        },
        status=200
    )
    testapp.post_json(reference_file['@id'] + '@@upload', {}, status=403)


def test_upload_credentials_forbidden_when_externally_hosted(testapp, externally_hosted_sequence_file):
    testapp.post_json(externally_hosted_sequence_file['@id'] + '@@upload', {}, status=403)


def test_upload_credentials_allowed_when_status_is_in_progress(testapp, reference_file):
    testapp.patch_json(
        reference_file['@id'],
        {
            'status': 'in progress',
            'upload_status': 'pending',
            'file_size': 123,
        },
        status=200
    )
    testapp.post_json(reference_file['@id'] + '@@upload', {}, status=200)


def test_upload_credentials_allowed_when_status_is_preview(testapp, reference_file):
    testapp.patch_json(
        reference_file['@id'],
        {
            'status': 'preview',
            'upload_status': 'pending',
            'file_size': 123,
        },
        status=200
    )
    testapp.post_json(reference_file['@id'] + '@@upload', {}, status=200)


def test_download_forbidden_when_externally_hosted(testapp, externally_hosted_sequence_file):
    testapp.get(externally_hosted_sequence_file['@id'] + '@@download', status=403)


@pytest.mark.parametrize(
    'file_status',
    [
        status
        for status in File.public_s3_statuses
    ]
)
def test_public_file_not_in_correct_bucket(testapp, root, dummy_request, signal_file_with_external_sheet, file_status):
    testapp.patch_json(
        signal_file_with_external_sheet['@id'],
        {
            'status': file_status,
            'release_timestamp': '2024-05-31T12:34:56Z',
            'upload_status': 'validated',

        }
    )
    file_item = root.get_by_uuid(signal_file_with_external_sheet['uuid'])
    external = file_item._get_external_sheet()
    assert external.get('bucket') == 'igvf-files-local'
    result, current_path, destination_path = file_item._file_in_correct_bucket(dummy_request)
    assert result is False
    assert current_path == 's3://igvf-files-local/xyz.bigWig'
    assert destination_path == 's3://igvf-public-local/xyz.bigWig'
    file_item._set_external_sheet({'bucket': 'igvf-public-local'})
    result, current_path, destination_path = file_item._file_in_correct_bucket(dummy_request)
    assert result is True
    assert current_path == 's3://igvf-public-local/xyz.bigWig'
    assert destination_path == 's3://igvf-public-local/xyz.bigWig'


@pytest.mark.parametrize(
    'file_status',
    [
        status
        for status in File.private_s3_statuses
    ]
)
def test_private_file_not_in_correct_bucket(testapp, root, dummy_request, signal_file_with_external_sheet, file_status):
    if file_status == 'revoked':
        testapp.patch_json(
            signal_file_with_external_sheet['@id'],
            {
                'status': file_status,
                'upload_status': 'validated',
                'release_timestamp': '2024-05-31T12:34:56Z',
            }
        )
    else:
        testapp.patch_json(
            signal_file_with_external_sheet['@id'],
            {
                'status': file_status,
                'upload_status': 'validated',
            }
        )
    file_item = root.get_by_uuid(signal_file_with_external_sheet['uuid'])
    external = file_item._get_external_sheet()
    assert external.get('bucket') == 'igvf-files-local'
    result, current_path, destination_path = file_item._file_in_correct_bucket(dummy_request)
    assert result is False
    assert current_path == 's3://igvf-files-local/xyz.bigWig'
    assert destination_path == 's3://igvf-private-local/xyz.bigWig'
    file_item._set_external_sheet({'bucket': 'igvf-private-local'})
    result, current_path, destination_path = file_item._file_in_correct_bucket(dummy_request)
    assert result is True
    assert current_path == 's3://igvf-private-local/xyz.bigWig'
    assert destination_path == 's3://igvf-private-local/xyz.bigWig'


def test_file_in_correct_bucket_no_external_sheet(root, dummy_request, signal_file):
    file_item = root.get_by_uuid(signal_file['uuid'])
    result, current_path, destination_path = file_item._file_in_correct_bucket(dummy_request)
    assert result is True
    assert current_path is None
    assert destination_path is None


def test_file_in_correct_bucket_restricted_or_externally_hosted(testapp, root, dummy_request, sequence_file_with_external_sheet, controlled_sequence_file_with_external_sheet):
    testapp.patch_json(
        sequence_file_with_external_sheet['@id'],
        {
            'status': 'in progress',
            'upload_status': 'invalidated',
        }
    )
    file_item = root.get_by_uuid(sequence_file_with_external_sheet['uuid'])
    result, current_path, destination_path = file_item._file_in_correct_bucket(dummy_request)
    assert result is True
    assert current_path is None
    assert destination_path is None
    testapp.patch_json(
        sequence_file_with_external_sheet['@id'],
        {
            'status': 'in progress',
            'upload_status': 'validated',
        }
    )
    file_item = root.get_by_uuid(sequence_file_with_external_sheet['uuid'])
    result, current_path, destination_path = file_item._file_in_correct_bucket(dummy_request)
    assert result is False
    assert current_path == 's3://igvf-files-local/xyz.bigWig'
    assert destination_path == 's3://igvf-private-local/xyz.bigWig'
    testapp.patch_json(
        sequence_file_with_external_sheet['@id'],
        {
            'status': 'in progress',
            'upload_status': 'validation exempted',
        }
    )
    file_item = root.get_by_uuid(sequence_file_with_external_sheet['uuid'])
    result, current_path, destination_path = file_item._file_in_correct_bucket(dummy_request)
    assert result is False
    assert current_path == 's3://igvf-files-local/xyz.bigWig'
    assert destination_path == 's3://igvf-private-local/xyz.bigWig'
    testapp.patch_json(
        sequence_file_with_external_sheet['@id'],
        {
            'status': 'in progress',
            'upload_status': 'validation exempted',
            'externally_hosted': True,
            'external_host_url': 'https://example.com/file.fastq.gz',
        }
    )
    file_item = root.get_by_uuid(sequence_file_with_external_sheet['uuid'])
    result, current_path, destination_path = file_item._file_in_correct_bucket(dummy_request)
    assert result is True
    assert current_path is None
    assert destination_path is None
    testapp.patch_json(
        controlled_sequence_file_with_external_sheet['@id'],
        {
            'status': 'in progress',
            'upload_status': 'validation exempted',
        }
    )
    file_item = root.get_by_uuid(controlled_sequence_file_with_external_sheet['uuid'])
    result, current_path, destination_path = file_item._file_in_correct_bucket(dummy_request)
    assert result is True
    assert current_path is None
    assert destination_path is None


def test_file_update_bucket_as_admin(testapp, dummy_request, signal_file_with_external_sheet, submitter_testapp,):
    testapp.patch_json(
        signal_file_with_external_sheet['@id'],
        {
            'status': 'released',
            'release_timestamp': '2024-05-31T12:34:56Z',
            'upload_status': 'validated',
        }
    )
    res = testapp.patch_json(
        signal_file_with_external_sheet['@id'] + '@@update_bucket',
        {
            'new_bucket': 'igvf-public-local',
        }
    )
    assert res.json['old_bucket'] == 'igvf-files-local'
    assert res.json['new_bucket'] == 'igvf-public-local'
    # Reset
    res = testapp.patch_json(
        signal_file_with_external_sheet['@id'] + '@@update_bucket',
        {
            'new_bucket': 'igvf-files-local',
        }
    )
    # Unknown bucket
    testapp.patch_json(
        signal_file_with_external_sheet['@id'] + '@@update_bucket',
        {
            'new_bucket': 'unknown bucket'
        },
        status=422
    )
    # With force
    res = testapp.patch_json(
        signal_file_with_external_sheet['@id'] + '@@update_bucket?force=true',
        {
            'new_bucket': 'unknown bucket'
        }
    )
    assert res.json['old_bucket'] == 'igvf-files-local'
    assert res.json['new_bucket'] == 'unknown bucket'
    # As submitter
    submitter_testapp.patch_json(
        signal_file_with_external_sheet['@id'] + '@@update_bucket',
        {
            'new_bucket': 'unknown bucket'
        },
        status=403
    )


def test_file_reset_file_upload_bucket_on_upload_credentials(testapp, root, dummy_request, signal_file_with_external_sheet):
    testapp.patch_json(
        signal_file_with_external_sheet['@id'],
        {
            'status': 'in progress',
            'upload_status': 'validated',
        }
    )
    res = testapp.patch_json(
        signal_file_with_external_sheet['@id'] + '@@update_bucket',
        {
            'new_bucket': 'igvf-private-local'
        }
    )
    file_item = root.get_by_uuid(signal_file_with_external_sheet['uuid'])
    external = file_item._get_external_sheet()
    assert external.get('key') == 'xyz.bigWig'
    assert external.get('bucket') == 'igvf-private-local'
    testapp.patch_json(
        signal_file_with_external_sheet['@id'],
        {
            'upload_status': 'pending'
        }
    )
    file_item = root.get_by_uuid(signal_file_with_external_sheet['uuid'])
    res = testapp.post_json(signal_file_with_external_sheet['@id'] + '@@upload', {})
    file_item = root.get_by_uuid(signal_file_with_external_sheet['uuid'])
    external = file_item._get_external_sheet()
    assert external.get('bucket') == 'igvf-files-local'
    assert res.json['@graph'][0]['upload_credentials']['upload_url'] == 's3://igvf-files-local/xyz.bigWig'
