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
def configuration_file_seqspec_2(testapp, lab, award, measurement_set):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '8bbaaaea2cfba3b552a21c63a79f4543',
        'file_format': 'yaml',
        'file_set': measurement_set['@id'],
        'content_type': 'seqspec'
    }
    return testapp.post_json('/configuration_file', item).json['@graph'][0]


@pytest.fixture
def configuration_file_json(testapp, lab, award, measurement_set):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '0702dd4765dbc6ae2465a6cc8c3dc8c3',
        'file_format': 'json',
        'file_set': measurement_set['@id'],
        'content_type': 'scale factors'
    }
    return testapp.post_json('/configuration_file', item).json['@graph'][0]


@pytest.fixture
def configuration_file_v1(configuration_file_seqspec):
    item = configuration_file_seqspec.copy()
    item.update({
        'schema_version': '1',
        'dbxrefs': ['']
    })
    return item


@pytest.fixture
def configuration_file_v2(configuration_file_v1):
    item = configuration_file_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item


@pytest.fixture
def configuration_file_v3(configuration_file_v1):
    item = configuration_file_v1.copy()
    item.update({
        'schema_version': '3',
        'upload_status': 'pending',
        'status': 'released'
    })
    return item


@pytest.fixture
def configuration_file_v6(configuration_file_v1):
    item = configuration_file_v1.copy()
    item.update({
        'schema_version': '6',
        'seqspec_of': [],
        'derived_from': [],
        'file_format_specifications': []
    })
    return item
