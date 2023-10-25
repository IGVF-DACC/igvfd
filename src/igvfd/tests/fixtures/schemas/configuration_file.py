import pytest


@pytest.fixture
def configuration_file_seqspec(testapp, lab, award, measurement_set):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '05c12a287334386c94131ab8aa00d08a',
        'file_format': 'yaml',
        'file_set': measurement_set['@id'],
        'content_type': 'seqspec'
    }
    return testapp.post_json('/configuration_file', item).json['@graph'][0]


@pytest.fixture
def configuration_file_v2(configuration_file):
    item = configuration_file.copy()
    item.update({
        'schema_version': '2',
        'dbxrefs': ['']
    })
    return item
