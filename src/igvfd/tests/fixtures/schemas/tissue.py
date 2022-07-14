import pytest


@pytest.fixture
def tissue(testapp, lab, source, award, rodent_donor):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Mus musculus',
        'donors': [rodent_donor['@id']]
    }
    return testapp.post_json('/tissue', item, status=201).json['@graph'][0]


@pytest.fixture
def tissue_1(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '1'
    })
    return item


@pytest.fixture
def tissue_part_of(tissue):
    item = tissue.copy()
    item.update({
        'aliases': 'igvf-dacc:tissue_part_of'
    })
    return item
