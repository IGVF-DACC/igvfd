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
        'dimension_x': 'cell',
        'dimension_y': ['gene']
    }
    return testapp.post_json('/matrix_file', item, status=201).json['@graph'][0]


@pytest.fixture
def matrix_file_hic(testapp, lab, award, measurement_set, reference_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '7b75ce0d0c2b2fc337145cb471d02dce',
        'file_format': 'hic',
        'file_set': measurement_set['@id'],
        'file_size': 512355134,
        'content_type': 'contact matrix',
        'reference_files': [
            reference_file['@id']
        ],
        'dimension_x': 'genomic position',
        'dimension_y': ['genomic position']
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


@pytest.fixture
def matrix_file_v3(matrix_file_v1):
    item = matrix_file_v1.copy()
    item.update({
        'schema_version': '3',
        'upload_status': 'pending',
        'status': 'released'
    })
    return item


@pytest.fixture
def matrix_file_v5(matrix_file_v1):
    item = matrix_file_v1.copy()
    item.update({
        'schema_version': '5',
        'derived_from': [],
        'file_format_specifications': []
    })
    return item


@pytest.fixture
def matrix_file_v6(matrix_file_v1):
    item = matrix_file_v1.copy()
    item.update({
        'schema_version': '6',
        'dimension1': 'cell',
        'dimension2': 'gene'
    })
    return item
