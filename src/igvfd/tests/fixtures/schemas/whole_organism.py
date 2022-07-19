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
def whole_organism_1(whole_organism):
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
def whole_organism_2(whole_organism):
    item = whole_organism.copy()
    item.update({
        'schema_version': '2',
        'aliases': [],
    })
    return item
