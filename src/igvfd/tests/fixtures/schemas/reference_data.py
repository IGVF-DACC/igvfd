import pytest


@pytest.fixture
def reference_data(testapp, lab, award, analysis_set_with_sample):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '515c8a6af303ea86bc59c629ff198278',
        'file_format': 'fasta',
        'file_set': analysis_set_with_sample['@id'],
        'content_type': 'exclusion list'
    }
    return testapp.post_json('/reference_data', item, status=201).json['@graph'][0]


@pytest.fixture
def reference_data_v1(reference_data, document_v1):
    item = reference_data.copy()
    item.update({
        'schema_version': '1',
        'aliases': ['igvf:reference_data_v1'],
        'collections': ['ENCODE'],
        'documents': [document_v1['@id']],
        'alternate_accessions': ['IGVFFF000ATQ']
    })
    return item
