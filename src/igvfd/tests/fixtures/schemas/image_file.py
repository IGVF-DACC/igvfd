import pytest


@pytest.fixture
def image_file(testapp, lab, award, analysis_set_with_sample):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'f5c708c9e1ff19af0a130d71b52c485a',
        'file_format': 'jpg',
        'file_set': analysis_set_with_sample['@id'],
        'file_size': 8491803,
        'content_type': 'detected tissue'
    }
    return testapp.post_json('/image_file', item, status=201).json['@graph'][0]


@pytest.fixture
def image_file_v3(image_file):
    item = image_file.copy()
    item.update({
        'schema_version': '3',
        'derived_from': [],
        'file_format_specifications': []
    })
    return item
