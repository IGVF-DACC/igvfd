import pytest


@pytest.fixture
def whole_organism(testapp, lab, source, award, rodent_donor):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Mus musculus',
        'donors': [rodent_donor['@id']]
    }
    return testapp.post_json('/whole_organism', item, status=201).json['@graph'][0]


@pytest.fixture
def whole_organism_v1(whole_organism):
    item = whole_organism.copy()
    item.update({
        'schema_version': '1'
    })
    return item


@pytest.fixture
def whole_organism_part_of(whole_organism):
    item = whole_organism.copy()
    return item


@pytest.fixture
def whole_organism_v2(whole_organism):
    item = whole_organism.copy()
    item.update({
        'schema_version': '2',
        'aliases': [],
        'donors': [],
        'dbxrefs': [],
        'collections': [],
        'alternate_accessions': [],
        'treatments': []
    })
    return item


@pytest.fixture
def whole_organism_v3(whole_organism, phenotype_term_alzheimers):
    item = whole_organism.copy()
    item.update({
        'schema_version': '3',
        'disease_term': phenotype_term_alzheimers['@id']
    })
    return item
