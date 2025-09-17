import pytest


@pytest.fixture
def signal_file(testapp, lab, award, principal_analysis_set, reference_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '350e99db0738e1987d3d6b53c22c3937',
        'file_format': 'bigWig',
        'file_set': principal_analysis_set['@id'],
        'file_size': 4328491803,
        'content_type': 'signal of all reads',
        'reference_files': [
            reference_file['@id']
        ],
        'strand_specificity': 'plus',
        'normalized': False,
        'filtered': False
    }
    return testapp.post_json('/signal_file', item, status=201).json['@graph'][0]


@pytest.fixture
def signal_file_with_external_sheet(signal_file, root):
    file_item = root.get_by_uuid(signal_file['uuid'])
    properties = file_item.upgrade_properties()
    file_item.update(
        properties,
        sheets={
            'external': {
                'service': 's3',
                'key': 'xyz.bigWig',
                'bucket': 'igvf-files-local',
            }
        }
    )
    return signal_file


@pytest.fixture
def signal_file_v1(signal_file):
    item = signal_file.copy()
    item.update({
        'schema_version': '1',
        'dbxrefs': ['']
    })
    return item


@pytest.fixture
def signal_file_v2(signal_file_v1):
    item = signal_file_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item


@pytest.fixture
def signal_file_v3(signal_file_v1):
    item = signal_file_v1.copy()
    item.update({
        'schema_version': '3',
        'upload_status': 'pending',
        'status': 'released'
    })
    return item


@pytest.fixture
def signal_file_v4(testapp, lab, award, principal_analysis_set, reference_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'b9d3d6e1c3b0793dc09853c229675937',
        'file_format': 'bigWig',
        'file_set': principal_analysis_set['@id'],
        'file_size': 4328491803,
        'content_type': 'signal of all reads',
        'reference_files': [
            reference_file['@id']
        ],
        'strand_specificity': 'plus',
        'normalized': False,
        'filtered': False,
        'schema_version': '4'
    }
    return item


@pytest.fixture
def signal_file_v5(signal_file):
    item = signal_file.copy()
    item.update({
        'assembly': 'mm10',
        'schema_version': '5'
    })
    return item


@pytest.fixture
def signal_file_v7(signal_file):
    item = signal_file.copy()
    item.update({
        'derived_from': [],
        'file_format_specifications': [],
        'schema_version': '7'
    })
    return item


@pytest.fixture
def signal_file_v8(signal_file):
    item = signal_file.copy()
    item.update({
        'schema_version': '8',
        'content_type': 'fold over change control'
    })
    return item


@pytest.fixture
def signal_file_v10(signal_file):
    item = signal_file.copy()
    item.update({
        'schema_version': '10',
    })
    return item


@pytest.fixture
def signal_file_v11(testapp, lab, award, principal_analysis_set, reference_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '350e99db0738e1987d3d6b53c22c3937',
        'file_format': 'bigWig',
        'file_set': principal_analysis_set['@id'],
        'file_size': 4328491803,
        'content_type': 'signal of all reads',
        'reference_files': [
            reference_file['@id']
        ],
        'strand_specificity': 'plus',
        'filtered': False
    }
    return testapp.post_json('/signal_file', item, status=201).json['@graph'][0]


@pytest.fixture
def signal_file_v12(signal_file):
    item = signal_file.copy()
    item.update({
        'schema_version': '12',
        'assembly': 'GRCh38',
        'transcriptome_annotation': 'GENCODE 40'
    })
    return item
