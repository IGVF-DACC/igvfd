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
def technical_sample_v4(technical_sample):
    item = technical_sample.copy()
    item.update({
        'schema_version': '4',
        'accession': 'IGVFSM111TTT'
    })
    return item


@pytest.fixture
def technical_sample_v5(technical_sample):
    item = technical_sample.copy()
    item.update({
        'schema_version': '5',
        'sorted_fraction': '/in_vitro_system/3de8faf0-7a25-11ed-a1eb-0242ac120002/'
    })
    return item


@pytest.fixture
def technical_sample_v6(technical_sample):
    item = technical_sample.copy()
    item.update({
        'schema_version': '6',
        'sorted_fraction': '/in_vitro_system/3de8faf0-7a25-11ed-a1eb-0242ac120002/'
    })
    return item


@pytest.fixture
def technical_sample_v7(lab, award, source, sample_term_adrenal_gland, crispr_modification):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'technical_sample_term': sample_term_adrenal_gland['@id'],
        'modification': crispr_modification['@id']
    }
    return item


@pytest.fixture
def technical_sample_v8_no_units(technical_sample):
    item = technical_sample.copy()
    item.update({
        'schema_version': '8',
        'starting_amount': 5
    })
    return item


@pytest.fixture
def technical_sample_v8_no_amount(technical_sample):
    item = technical_sample.copy()
    item.update({
        'schema_version': '8',
        'starting_amount_units': 'g'
    })
    return item


@pytest.fixture
def technical_sample_v9(technical_sample, in_vitro_differentiated_cell):
    item = technical_sample.copy()
    item.update({
        'schema_version': '9',
        'sorted_fraction': in_vitro_differentiated_cell['@id'],
        'sorted_fraction_detail': 'This is a detail about the sorting.'
    })
    return item


@pytest.fixture
def technical_sample_v10(technical_sample_v9):
    item = technical_sample_v9.copy()
    item.update({
        'schema_version': '10',
        'description': ''
    })
    return item


@pytest.fixture
def technical_sample_v12(testapp, other_lab, award, sample_term_technical_sample):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'product_id': '100A',
        'sample_material': 'synthetic',
        'sample_terms': [sample_term_technical_sample['@id']]
    }
    return item
