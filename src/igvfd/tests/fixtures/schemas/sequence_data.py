import pytest


@pytest.fixture
def sequence_data(testapp, lab, award, analysis_set_with_sample):
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
        'content_type': 'reads'
    }
    return testapp.post_json('/sequence_data', item, status=201).json['@graph'][0]


@pytest.fixture
def sequence_data_fastq_no_read_length(testapp, lab, award, analysis_set_with_sample):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'cb888dc8d303ea1b7959c698e819c0f1',
        'file_format': 'fastq',
        'file_set': analysis_set_with_sample['@id'],
        'content_type': 'reads'
    }
    return item
