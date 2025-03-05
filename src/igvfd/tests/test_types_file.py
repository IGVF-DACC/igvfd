import pytest


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
        status=422
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
    assert 's3_uri' not in res.json
    assert 'href' not in res.json
    assert 'anvil_url' in res.json
    testapp.get(controlled_access_alignment_file['@id'] + '@@download', status=403)


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
    genome_browser_annotation_file,
    image_file,
    matrix_file,
    model_file,
    reference_file,
    sequence_file,
    signal_file,
    tabular_file,
    base_prediction_set
):
    testapp.patch_json(
        alignment_file['@id'],
        {
            'transcriptome_annotation': 'GENCODE 43',
            'redacted': True
        }
    )
    res = testapp.get(alignment_file['@id'])
    assert res.json.get('summary', '') == 'GRCh38 GENCODE 43 unfiltered redacted alignments'

    testapp.patch_json(
        genome_browser_annotation_file['@id'],
        {
            'assembly': 'GRCh38',
            'transcriptome_annotation': 'GENCODE 43'
        }
    )
    res = testapp.get(genome_browser_annotation_file['@id'])
    assert res.json.get('summary', '') == 'GRCh38 GENCODE 43 peaks'

    res = testapp.get(image_file['@id'])
    assert res.json.get('summary', '') == 'detected tissue'

    res = testapp.get(matrix_file['@id'])
    assert res.json.get('summary', '') == 'cell by gene in sparse gene count matrix'

    res = testapp.get(model_file['@id'])
    assert res.json.get('summary', '') == 'graph structure'

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

    testapp.patch_json(
        sequence_file['@id'],
        {
            'illumina_read_type': 'R2'
        }
    )
    res_sequence_file = testapp.get(sequence_file['@id'])
    assert res_sequence_file.json.get('summary', '') == 'R2 reads from sequencing run 1'

    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file['@id']]
        }
    )
    res = testapp.get(configuration_file_seqspec['@id'])
    assert res.json.get('summary', '') == f'seqspec of {res_sequence_file.json.get("accession")}'

    testapp.patch_json(
        signal_file['@id'],
        {
            'normalized': True,
            'filtered': True,
            'transcriptome_annotation': 'GENCODE 43'
        }
    )
    res = testapp.get(signal_file['@id'])
    assert res.json.get('summary', '') == 'GRCh38 GENCODE 43 filtered normalized plus strand signal of all reads'

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
    measurement_set,
    measurement_set_multiome,
    analysis_set_base,
    base_auxiliary_set
):
    testapp.patch_json(
        alignment_file['@id'],
        {
            'file_set': measurement_set['@id']
        }
    )
    res = testapp.get(alignment_file['@id'])
    assert set(res.json.get('assay_titles', [])) == {'SUPERSTARR'}
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [measurement_set['@id'], measurement_set_multiome['@id']]
        }
    )
    testapp.patch_json(
        alignment_file['@id'],
        {
            'file_set': analysis_set_base['@id']
        }
    )
    res = testapp.get(alignment_file['@id'])
    assert set(res.json.get('assay_titles', [])) == {'SUPERSTARR', '10x multiome'}
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']],
            'preferred_assay_title': '10x multiome with MULTI-seq'
        }
    )
    testapp.patch_json(
        alignment_file['@id'],
        {
            'file_set': base_auxiliary_set['@id']
        }
    )
    res = testapp.get(alignment_file['@id'])
    assert set(res.json.get('assay_titles', [])) == {'10x multiome with MULTI-seq'}


def test_file_workflow(
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
    assert res.json.get('workflow', '')['@id'] == base_workflow['@id']


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
