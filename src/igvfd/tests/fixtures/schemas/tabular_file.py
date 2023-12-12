import pytest


@pytest.fixture
def tabular_file(testapp, lab, award, analysis_set_with_sample):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '01b08bb5485ac730df19af55ba4bb09c',
        'file_format': 'tsv',
        'file_set': analysis_set_with_sample['@id'],
        'upload_storage_service': 's3',
        'content_type': 'peaks'
    }
    return testapp.post_json('/tabular_file', item, status=201).json['@graph'][0]


@pytest.fixture
def tabular_file_v1(tabular_file):
    item = tabular_file.copy()
    item.update({
        'schema_version': '1',
        'dbxrefs': ['']
    })
    return item


@pytest.fixture
def tabular_file_v2(tabular_file_v1):
    item = tabular_file_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item


@pytest.fixture
def tabular_file_v3(tabular_file_v1):
    item = tabular_file_v1.copy()
    item.update({
        'schema_version': '3',
        'upload_status': 'pending',
        'status': 'released'
    })
    return item
