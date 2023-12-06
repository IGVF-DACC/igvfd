import pytest


@pytest.fixture
def signal_file(testapp, lab, award, analysis_set_with_sample, reference_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '350e99db0738e1987d3d6b53c22c3937',
        'file_format': 'bigWig',
        'file_set': analysis_set_with_sample['@id'],
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
