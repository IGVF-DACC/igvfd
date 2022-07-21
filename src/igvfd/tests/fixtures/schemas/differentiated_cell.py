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
        'aliases': 'igvf-dacc:differentiated_cell_part_of',
        'schema_version': '2',
        'dbxrefs': []
    })
    return item


@pytest.fixture
def differentiated_cell_2(differentiated_cell):
    item = differentiated_cell.copy()
    item.update({
        'schema_version': '2'
    })
    return item


@pytest.fixture
def differentiated_cell_3(differentiated_cell):
    item = differentiated_cell.copy()
    item.update({
        'schema_version': '3',
        'dbxrefs': []
    })
    return item


@pytest.fixture
def differentiated_cell_4(differentiated_cell):
    item = differentiated_cell.copy()
    item.update({
        'schema_version': '4',
        'post_differentiation_time': 10,
        'post_differentiation_time_units': 'stage'
    })
    return item


@pytest.fixture
def differentiated_cell_4_good_value(differentiated_cell):
    item = differentiated_cell.copy()
    item.update({
        'schema_version': '4',
        'post_differentiation_time': 7,
        'post_differentiation_time_units': 'month'
    })
    return item


@pytest.fixture
def differentiated_cell_4_with_note(differentiated_cell):
    item = differentiated_cell.copy()
    item.update({
        'schema_version': '4',
        'post_differentiation_time': 10,
        'post_differentiation_time_units': 'stage',
        'notes': 'This is a note.'
    })
    return item

