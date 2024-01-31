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
