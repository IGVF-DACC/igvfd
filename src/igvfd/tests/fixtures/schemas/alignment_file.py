import pytest


@pytest.fixture
def alignment_file(testapp, lab, award, analysis_set_with_sample, reference_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'dc8d8a6af6105a86bc51c389ff19ea1b',
        'file_format': 'bam',
        'file_set': analysis_set_with_sample['@id'],
        'file_size': 8491803,
        'content_type': 'alignments',
        'reference_files': [
            reference_file['@id']
        ],
        'redacted': False,
        'filtered': False
    }
    return testapp.post_json('/alignment_file', item, status=201).json['@graph'][0]


@pytest.fixture
def alignment_file_v2(alignment_file):
    item = alignment_file.copy()
    item.update({
        'schema_version': '2',
        'dbxrefs': ['']
    })
    return item
