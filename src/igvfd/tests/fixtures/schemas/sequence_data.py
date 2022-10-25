import pytest


@pytest.fixture
def sequence_data(testapp, lab, award, analysis_set_with_sample):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '515c8a6af303ea86bc59c629ff198277',
        'file_format': 'fastq',
        'file_set': analysis_set_with_sample['@id'],
        'content_type': 'reads'
    }
    return testapp.post_json('/sequence_data', item, status=201).json['@graph'][0]


@pytest.fixture
def sequence_data_paired_end_1(testapp, lab, award, analysis_set_with_sample):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'd9208a6af38f0886bc59c629ff19e5c0',
        'file_format': 'fastq',
        'file_set': analysis_set_with_sample['@id'],
        'content_type': 'reads',
        'run_type': 'paired-ended',
        'paired_end': '1'
    }
    return testapp.post_json('/sequence_data', item, status=201).json['@graph'][0]
