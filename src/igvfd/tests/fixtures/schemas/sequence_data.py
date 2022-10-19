import pytest


@pytest.fixture
def sequence_data(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '515c8a6af303ea86bc59c629ff198277',
        'file_format': 'fastq',
        'content_type': 'reads'
    }
    return testapp.post_json('/sequence_data', item, status=201).json['@graph'][0]


@pytest.fixture
def sequence_data_paired_end_1(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '515c8a6af303ea86bc59c629ff198277',
        'file_format': 'fastq',
        'content_type': 'reads',
        'run_type': 'paired-ended',
        'paired_end': '1'
    }
    return testapp.post_json('/sequence_data', item, status=201).json['@graph'][0]
