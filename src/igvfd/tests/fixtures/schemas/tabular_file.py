import pytest


@pytest.fixture
def tabular_file(testapp, lab, award, analysis_set_with_sample):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '01b08bb5485ac730df19af55ba4bb09c',
        'file_format': 'tsv',
        'file_set': analysis_set_with_sample['@id'],
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
