import pytest


@pytest.fixture
def reference_data(testapp, award, lab, attachment):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': attachment['md5sum'],
        'file_format': 'gtf',
        'file_set': 'igvf:analysis_set_1',
        'content_type': 'transcriptome reference',
        'assembly': 'GRCh38'
    }
    return item


@pytest.fixture
def reference_data_1(testapp):
    item = {
        'file_format': 'gtf',
        'file_set': 'igvf:analysis_set_1',
        'content_type': 'transcriptome reference',
        'assembly': 'GRCh38'
    }
    return testapp.post_json('/reference_data', item, status=201).json['@graph'][0]
