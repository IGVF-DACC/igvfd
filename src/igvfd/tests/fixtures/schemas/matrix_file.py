import pytest


@pytest.fixture
def matrix_file(testapp, lab, award, analysis_set_with_sample, reference_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '01b08bb5485ac730df19af55ba4bb01c',
        'file_format': 'hdf5',
        'file_set': analysis_set_with_sample['@id'],
        'file_size': 8491803,
        'content_type': 'sparse gene count matrix',
        'reference_files': [
            reference_file['@id']
        ],
        'dimension1': 'cell',
        'dimension2': 'gene'
    }
    return testapp.post_json('/matrix_file', item, status=201).json['@graph'][0]


@pytest.fixture
def matrix_file_v1(matrix_file):
    item = matrix_file.copy()
    item.update({
        'schema_version': '1',
        'dbxrefs': ['']
    })
    return item


@pytest.fixture
def matrix_file_v2(matrix_file_v1):
    item = matrix_file_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item
