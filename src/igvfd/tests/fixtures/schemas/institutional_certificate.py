import pytest


@pytest.fixture
def institutional_certificate(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'urls': ['https://drive.google.com/file/example-url-123'],
        'certificate_identifier': 'IP123-45',
        'controlled_access': False
    }
    return testapp.post_json('/institutional_certificate', item).json['@graph'][0]


@pytest.fixture
def institutional_certificate_controlled(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'urls': ['https://drive.google.com/file/example-url-123'],
        'data_use_limitation': 'GRU',
        'certificate_identifier': 'IP321-45',
        'controlled_access': True
    }
    return testapp.post_json('/institutional_certificate', item).json['@graph'][0]


@pytest.fixture
def institutional_certificate_controlled_access(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'urls': ['https://drive.google.com/file/example-url-456'],
        'certificate_identifier': 'IP100-99',
        'controlled_access': True,
        'data_use_limitation': 'GRU'
    }
    return testapp.post_json('/institutional_certificate', item).json['@graph'][0]
