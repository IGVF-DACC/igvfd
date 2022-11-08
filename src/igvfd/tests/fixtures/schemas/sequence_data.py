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
