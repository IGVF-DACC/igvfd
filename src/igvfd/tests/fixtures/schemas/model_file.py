import pytest


@pytest.fixture
def model_file(testapp, lab, award, principal_analysis_set):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '1b4376ef56901e05c708c930d1173f5a',
        'file_format': 'json',
        'file_set': principal_analysis_set['@id'],
        'file_size': 289153,
        'content_type': 'graph structure',
        'controlled_access': False
    }
    return testapp.post_json('/model_file', item, status=201).json['@graph'][0]


@pytest.fixture
def model_file_v2(model_file):
    item = model_file.copy()
    item.update({
        'schema_version': '2',
        'status': 'replaced'
    })
    return item
