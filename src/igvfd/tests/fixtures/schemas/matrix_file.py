import pytest


@pytest.fixture
def alignment_file(testapp, lab, award, analysis_set_with_sample, reference_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'b64eed10-78b9-4674-95e5-dae39f35f132',
        'file_format': 'hdf5',
        'file_set': analysis_set_with_sample['@id'],
        'file_size': 8491803,
        'content_type': 'parse gene count matrix',
        'reference_files': [
            reference_file['@id']
        ],
        'dimension1': 'cell',
        'dimension2': 'gene'
    }
    return testapp.post_json('/matrix_file', item, status=201).json['@graph'][0]
