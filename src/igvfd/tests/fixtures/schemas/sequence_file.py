import pytest


@pytest.fixture
def sequence_file(
        testapp, lab, award, analysis_set_with_sample, platform_term_HiSeq):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '525c8a6af303ea86bc59c629ff198277',
        'file_format': 'fastq',
        'file_set': analysis_set_with_sample['@id'],
        'minimum_read_length': 99,
        'maximum_read_length': 101,
        'mean_read_length': 100,
        'read_count': 23040138,
        'file_size': 5495803,
        'content_type': 'reads',
        'sequencing_run': 1,
        'sequencing_platform': platform_term_HiSeq['@id']
    }
    return testapp.post_json('/sequence_file', item, status=201).json['@graph'][0]


@pytest.fixture
def sequence_file_s3_uri(
        testapp, lab, award, analysis_set_with_sample, platform_term_HiSeq):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '515c8a6af303ea86bc59c629ff198277',
        'file_format': 'fastq',
        'file_set': analysis_set_with_sample['@id'],
        'minimum_read_length': 99,
        'maximum_read_length': 101,
        'mean_read_length': 100,
        'read_count': 23040138,
        'file_size': 5495803,
        'content_type': 'reads',
        'sequencing_run': 1,
        's3_uri': 's3://foo/bar/baz.fastq.gz',
        'sequencing_platform': platform_term_HiSeq['@id']
    }
    return testapp.post_json('/sequence_file', item, status=201).json['@graph'][0]


@pytest.fixture
def sequence_file_fastq_no_read_length(
        testapp, lab, award, analysis_set_with_sample, platform_term_HiSeq):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'cb888dc8d303ea1b7959c698e819c0f1',
        'file_format': 'fastq',
        'file_set': analysis_set_with_sample['@id'],
        'content_type': 'reads',
        'sequencing_run': 1,
        'sequencing_platform': platform_term_HiSeq['@id']
    }
    return item


@pytest.fixture
def sequence_file_sequencing_run_2(
        testapp, lab, award, analysis_set_with_sample, platform_term_HiSeq):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'aece2d0a32bcaa86b23d5a33ff198917',
        'file_format': 'fastq',
        'file_set': analysis_set_with_sample['@id'],
        'minimum_read_length': 99,
        'maximum_read_length': 101,
        'mean_read_length': 100,
        'read_count': 23040138,
        'file_size': 5495803,
        'content_type': 'reads',
        'sequencing_run': 2,
        'sequencing_platform': platform_term_HiSeq['@id']
    }
    return testapp.post_json('/sequence_file', item, status=201).json['@graph'][0]


@pytest.fixture
def sequence_file_v1(sequence_file):
    item = sequence_file.copy()
    item.update({
        'schema_version': '1',
        'accession': 'IGVFFF999AAA'
    })
    return item


@pytest.fixture
def sequence_file_v2(
        testapp, lab, award, analysis_set_with_sample):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'cb888dc8d303ea1b7959c698e819c0f1',
        'file_format': 'fastq',
        'file_set': analysis_set_with_sample['@id'],
        'content_type': 'reads',
        'sequencing_run': 1
    }
    return item


@pytest.fixture
def sequence_file_v3(sequence_file):
    item = sequence_file.copy()
    item.update({
        'schema_version': '3',
        'min_read_length': 300000001,
        'max_read_length': 5243061353423434123436423,
        'mean_read_length': 12345678910
    })
    return item
