import pytest


@pytest.fixture
def technical_sample(testapp, other_lab, award, source, sample_term_technical_sample):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'source': source['@id'],
        'sample_material': 'synthetic',
        'technical_sample_term': sample_term_technical_sample['@id']
    }
    return testapp.post_json('/technical_sample', item, status=201).json['@graph'][0]


@pytest.fixture
def technical_sample_v1(technical_sample):
    item = technical_sample.copy()
    item.update({
        'schema_version': '1',
        'dbxrefs': [],
        'aliases': [],
        'alternate_accessions': []
    })
    return item


@pytest.fixture
def technical_sample_v2(technical_sample):
    item = technical_sample.copy()
    item.update({
        'schema_version': '2',
        'additional_description': 'This is a description.'
    })
    return item


@pytest.fixture
def technical_sample_v3(technical_sample):
    item = technical_sample.copy()
    item.update({
        'schema_version': '3'
    })
    return item


@pytest.fixture
def technical_sample_v4(technical_sample, document_v1):
    item = technical_sample.copy()
    item.update({
        'schema_version': '4',
        'aliases': ['igvf:technical_sample_v4'],
        'alternate_accessions': ['IGVFSM666AAA'],
        'collections': ['ENCODE'],
        'documents': [document_v1['@id']],
        'dbxrefs': ['GEO:SAMN2']
    })
    return item
