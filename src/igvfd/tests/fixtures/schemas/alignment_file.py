import pytest


@pytest.fixture
def alignment_file(testapp, lab, award, principal_analysis_set, reference_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'dc8d8a6af6105a86bc51c389ff19ea1b',
        'file_format': 'bam',
        'file_set': principal_analysis_set['@id'],
        'file_size': 8491803,
        'content_type': 'alignments',
        'reference_files': [
            reference_file['@id']
        ],
        'redacted': False,
        'filtered': False,
        'controlled_access': False
    }
    return testapp.post_json('/alignment_file', item, status=201).json['@graph'][0]


@pytest.fixture
def controlled_access_alignment_file(testapp, lab, award, principal_analysis_set, reference_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'ec8d8a6af6105a86bc51c389ff19ea1b',
        'file_format': 'bam',
        'file_set': principal_analysis_set['@id'],
        'file_size': 9491803,
        'content_type': 'alignments',
        'reference_files': [
            reference_file['@id']
        ],
        'redacted': False,
        'filtered': False,
        'controlled_access': True,
    }
    return testapp.post_json('/alignment_file', item, status=201).json['@graph'][0]


@pytest.fixture
def alignment_file_v1(alignment_file):
    item = alignment_file.copy()
    item.update({
        'schema_version': '1',
        'dbxrefs': ['']
    })
    return item


@pytest.fixture
def alignment_file_v2(alignment_file_v1):
    item = alignment_file_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item


@pytest.fixture
def alignment_file_v3(alignment_file_v1):
    item = alignment_file_v1.copy()
    item.update({
        'schema_version': '3',
        'upload_status': 'pending',
        'status': 'released'
    })
    return item


@pytest.fixture
def alignment_file_v4(testapp, lab, award, principal_analysis_set, reference_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '9ea1d1ca6cd01ad85a8f6c86bc528d1b',
        'file_format': 'bam',
        'file_set': principal_analysis_set['@id'],
        'file_size': 8491803,
        'content_type': 'alignments',
        'reference_files': [
            reference_file['@id']
        ],
        'redacted': False,
        'filtered': False,
        'schema_version': '4'
    }
    return item


@pytest.fixture
def alignment_file_v5(alignment_file):
    item = alignment_file.copy()
    item.update({
        'assembly': 'mm10',
        'schema_version': '5'
    })
    return item


@pytest.fixture
def alignment_file_v7(alignment_file):
    item = alignment_file.copy()
    item.update({
        'derived_from': [],
        'file_format_specifications': [],
        'schema_version': '7'
    })
    return item


@pytest.fixture
def alignment_file_v8(alignment_file):
    item = alignment_file.copy()
    item.update({
        'schema_version': '8'
    })
    return item


@pytest.fixture
def alignment_file_v9(alignment_file):
    item = alignment_file.copy()
    item.update({
        'schema_version': '9',
        'controlled_access': True,
        'upload_status': 'deposited',
        'status': 'released',
        'release_timestamp': '2024-05-31T12:34:56Z',
        'anvil_source_url': 'http://abc.123',
    })
    return item


@pytest.fixture
def alignment_file_v10(alignment_file):
    item = alignment_file.copy()
    item.update({
        'schema_version': '10',
        'file_format': 'bai'
    })
    return item


@pytest.fixture
def alignment_file_v11(testapp, lab, award, principal_analysis_set, reference_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '5a159214b169da90d96590d47fff379e',
        'file_format': 'bam',
        'file_set': principal_analysis_set['@id'],
        'file_size': 8491803,
        'content_type': 'alignments',
        'reference_files': [
            reference_file['@id']
        ],
        'redacted': False,
        'filtered': False,
        'controlled_access': False
    }
    return item


@pytest.fixture
def alignment_file_v12(alignment_file):
    item = alignment_file.copy()
    item.update(
        {
            'schema_version': '12',
            'read_count':  23040138.0,
        }
    )
    return item


@pytest.fixture
def alignment_file_v13(alignment_file):
    item = alignment_file.copy()
    item.update(
        {
            'schema_version': '13',
            'assembly': 'GRCh38, mm10',
            'transcriptome_annotation': 'GENCODE 28, GENCODE M17'
        }
    )
    return item


@pytest.fixture
def alignment_file_v14(alignment_file):
    item = alignment_file.copy()
    item.update({
        'schema_version': '14',
    })
    return item


@pytest.fixture
def alignment_file_v15(alignment_file):
    item = alignment_file.copy()
    item.update({
        'schema_version': '15',
    })
    return item


@pytest.fixture
def alignment_file_v16(alignment_file):
    item = alignment_file.copy()
    item.update({
        'schema_version': '16',
        'assembly': 'GRCh38',
        'transcriptome_annotation': 'GENCODE 40'
    })
    return item
