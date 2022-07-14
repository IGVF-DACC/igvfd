import pytest


@pytest.fixture
def differentiated_cell(testapp, lab, award, source, human_donor):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Homo sapiens',
        'donors': [human_donor['@id']]
    }
    return testapp.post_json('/differentiated_cell', item, status=201).json['@graph'][0]


@pytest.fixture
def differentiated_cell_1(differentiated_cell):
    item = differentiated_cell.copy()
    item.update({
        'schema_version': '1'
    })
    return item


@pytest.fixture
def differentiated_cell_part_of(differentiated_cell):
    item = differentiated_cell.copy()
    item.update({
        'aliases': 'igvf-dacc:differentiated_cell_part_of'
    })
    return item
