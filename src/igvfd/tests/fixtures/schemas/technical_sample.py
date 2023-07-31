import pytest


@pytest.fixture
def technical_sample(testapp, other_lab, award, source, sample_term_technical_sample):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'sources': [source['@id']],
        'sample_material': 'synthetic',
        'sample_terms': [sample_term_technical_sample['@id']]
    }
    return testapp.post_json('/technical_sample', item, status=201).json['@graph'][0]


@pytest.fixture
def technical_sample_v1(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '1',
        'dbxrefs': [],
        'aliases': [],
        'alternate_accessions': []
    })
    return item


@pytest.fixture
def technical_sample_v2(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '2',
        'additional_description': 'This is a description.'
    })
    return item


@pytest.fixture
def technical_sample_v3(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '3'
    })
    return item


@pytest.fixture
def technical_sample_v4(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '4',
        'accession': 'IGVFSM111TTT'
    })
    return item


@pytest.fixture
def technical_sample_v5(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '5',
        'sorted_fraction': '/in_vitro_system/3de8faf0-7a25-11ed-a1eb-0242ac120002/'
    })
    return item


@pytest.fixture
def technical_sample_v6(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '6',
        'sorted_fraction': '/in_vitro_system/3de8faf0-7a25-11ed-a1eb-0242ac120002/'
    })
    return item


@pytest.fixture
def technical_sample_v7(lab, award, source, sample_term_adrenal_gland, modification):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'technical_sample_term': sample_term_adrenal_gland['@id'],
        'modification': modification['@id']
    }
    return item
