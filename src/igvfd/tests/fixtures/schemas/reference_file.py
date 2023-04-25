import pytest


@pytest.fixture
def reference_file(testapp, lab, award, analysis_set_with_sample):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '7f1987dea86105dd9d2582c0a91c3156',
        'file_format': 'gtf',
        'file_set': analysis_set_with_sample['@id'],
        'content_type': 'transcriptome reference'
    }
    return testapp.post_json('/reference_file', item, status=201).json['@graph'][0]
