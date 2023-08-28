import pytest


@pytest.fixture
def delimited_file(testapp, lab, award, analysis_set_with_sample, reference_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'b64eed15-78b9-4674-95e9-eae39f35f132',
        'file_format': 'csv',
        'file_set': analysis_set_with_sample['@id'],
        'file_size': 849180,
        'content_type': 'gene quantifications',
        'reference_files': [
            reference_file['@id']
        ],
        'column_headers': 'cell,gene',
        'number_of_columns': 2
    }
    return testapp.post_json('/delimited_file', item, status=201).json['@graph'][0]
