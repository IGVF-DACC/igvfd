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
def sequence_file_pod5(
        testapp, lab, award, analysis_set_with_sample, platform_term_HiSeq):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'c9ba6af303e4b6bc59c629b6409040a7',
        'file_format': 'pod5',
        'file_set': analysis_set_with_sample['@id'],
        'read_count': 23040138,
        'file_size': 5495803,
        'content_type': 'Nanopore reads',
        'sequencing_run': 10,
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
        'minimum_read_length': 300000001,
        'maximum_read_length': 5243061353423434123436423,
        'mean_read_length': 12345678910
    })
    return item


@pytest.fixture
def sequence_file_v4(sequence_file):
    item = sequence_file.copy()
    item.update({
        'schema_version': '4',
        'dbxrefs': []
    })
    return item


@pytest.fixture
def sequence_file_v5(sequence_file_v4):
    item = sequence_file_v4.copy()
    item.update({
        'schema_version': '5',
        'description': ''
    })
    return item


@pytest.fixture
def sequence_file_v6(sequence_file_v4):
    item = sequence_file_v4.copy()
    item.update({
        'schema_version': '6',
        'upload_status': 'pending',
        'status': 'released'
    })
    return item


@pytest.fixture
def sequence_file_v7_v1(sequence_file):
    item = sequence_file.copy()
    item.update({
        'schema_version': '7',
        'content_type': 'subreads',
        'file_format': 'bam'
    })
    return item


@pytest.fixture
def sequence_file_v7_v2(sequence_file):
    item = sequence_file.copy()
    item.update({
        'schema_version': '7',
        'content_type': 'reads',
        'file_format': 'bam'
    })
    return item


@pytest.fixture
def sequence_file_v7_v3(sequence_file):
    item = sequence_file.copy()
    item.update({
        'schema_version': '7',
        'content_type': 'subreads',
        'file_format': 'fastq'
    })
    return item


@pytest.fixture
def sequence_file_v8(sequence_file, configuration_file_seqspec):
    item = sequence_file.copy()
    item.update({
        'schema_version': '8',
        'seqspec': configuration_file_seqspec['@id']
    })
    return item


@pytest.fixture
def sequence_file_v9(sequence_file):
    item = sequence_file.copy()
    item.update({
        'schema_version': '9',
        'status': 'revoked'
    })
    return item


@pytest.fixture
def sequence_file_v10(sequence_file):
    item = sequence_file.copy()
    item.update({
        'derived_from': [],
        'file_format_specifications': [],
        'schema_version': '10'
    })
    return item


@pytest.fixture
def sequence_file_v12(sequence_file):
    item = sequence_file.copy()
    item.update({
        'sequencing_kit': 'NovaSeq 6000 S4 Reagent Kit V1.5',
        'schema_version': '12'
    })
    return item


@pytest.fixture
def controlled_sequence_file(lab, award, analysis_set_with_sample, platform_term_HiSeq):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'cb818dc8d303ea1b7959c698e819c0f1',
        'file_format': 'fastq',
        'file_set': analysis_set_with_sample['@id'],
        'content_type': 'reads',
        'sequencing_run': 1,
        'sequencing_platform': platform_term_HiSeq['@id'],
        'controlled_access': True
    }
    return item


@pytest.fixture
def controlled_sequence_file_object(testapp, controlled_sequence_file):
    return testapp.post_json('/sequence_file', controlled_sequence_file, status=201).json['@graph'][0]
