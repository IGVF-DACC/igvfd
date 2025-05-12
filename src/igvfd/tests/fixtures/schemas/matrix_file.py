import pytest


@pytest.fixture
def matrix_file(testapp, lab, award, principal_analysis_set, reference_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '01b08bb5485ac730df19af55ba4bb01c',
        'file_format': 'hdf5',
        'file_set': principal_analysis_set['@id'],
        'file_size': 8491803,
        'content_type': 'sparse gene count matrix',
        'reference_files': [
            reference_file['@id']
        ],
        'principal_dimension': 'cell',
        'secondary_dimensions': ['gene']
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
        'principal_dimension': 'genomic position',
        'secondary_dimensions': ['genomic position']
    }
    return testapp.post_json('/matrix_file', item, status=201).json['@graph'][0]


@pytest.fixture
def matrix_file_with_base_workflow(testapp, lab, award, analysis_set_with_workflow, reference_file, analysis_step_version):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '2a304515e3f9a882b413b9965f4f4461',
        'file_format': 'hdf5',
        'file_set': analysis_set_with_workflow['@id'],
        'file_size': 7491803,
        'content_type': 'sparse gene count matrix',
        'reference_files': [
            reference_file['@id']
        ],
        'principal_dimension': 'cell',
        'secondary_dimensions': ['gene'],
        'analysis_step_version': analysis_step_version['@id']
    }
    return testapp.post_json('/matrix_file', item, status=201).json['@graph'][0]


@pytest.fixture
def matrix_file_with_base_workflow_2(testapp, lab, award, analysis_set_base, reference_file, analysis_step_version_2):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'a9ac1c24865c7183a0403bc8bc6c7599',
        'file_format': 'hdf5',
        'file_set': analysis_set_base['@id'],
        'file_size': 8491803,
        'content_type': 'sparse gene count matrix',
        'reference_files': [
            reference_file['@id']
        ],
        'principal_dimension': 'cell',
        'secondary_dimensions': ['gene'],
        'analysis_step_version': analysis_step_version_2['@id']
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
def matrix_file_v6(testapp, lab, award, measurement_set, reference_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'c9be16849c41ecc5c7ed8af9502358c7',
        'file_format': 'h5ad',
        'file_set': measurement_set['@id'],
        'file_size': 512355134,
        'content_type': 'contact matrix',
        'reference_files': [
            reference_file['@id']
        ],
        'schema_version': '6',
        'dimension1': 'cell',
        'dimension2': 'gene'
    }
    return item


@pytest.fixture
def matrix_file_v7(matrix_file):
    item = matrix_file.copy()
    item.update({
        'schema_version': '7',
        'content_type': 'comprehensive gene count matrix',
        'file_format': 'tar'
    })
    return item
