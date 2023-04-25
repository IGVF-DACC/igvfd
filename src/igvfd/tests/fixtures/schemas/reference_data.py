import pytest


@pytest.fixture
def reference_data(testapp, lab, award, analysis_set_with_sample):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '7f1987dea86105dd9d2582c0a91c3856',
        'file_format': 'gtf',
        'file_set': analysis_set_with_sample['@id'],
        'content_type': 'transcriptome reference'
    }
    return testapp.post_json('/reference_data', item, status=201).json['@graph'][0]


@pytest.fixture
def reference_data_v2(reference_data):
    item = reference_data.copy()
    item.update({
        'schema_version': '2'
    })
    return item
