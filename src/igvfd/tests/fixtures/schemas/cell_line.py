import pytest


@pytest.fixture
def cell_line(testapp, other_lab, award, rodent_donor):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'source': other_lab['@id'],
        'taxa': 'Mus musculus',
        'donors': [rodent_donor['@id']]
    }
    return testapp.post_json('/cell_line', item, status=201).json['@graph'][0]


@pytest.fixture
def cell_line_with_date_obtained(testapp, other_lab, award, human_donor):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'source': other_lab['@id'],
        'date_obtained': '2022-04-02',
        'taxa': 'Homo sapiens',
        'donors': [human_donor['@id']]
    }
    return testapp.post_json('/cell_line', item, status=201).json['@graph'][0]


@pytest.fixture
def cell_line_1(cell_line):
    item = cell_line.copy()
    item.update({
        'schema_version': '1'
    })
    return item


@pytest.fixture
def cell_line_part_of(cell_line):
    item = cell_line.copy()
    item.update({
        'aliases': 'igvf-dacc:cell_line_part_of'
    })
    return item


@pytest.fixture
def cell_line_2(cell_line):
    item = cell_line.copy()
    item.update({
        'schema_version': '2'
    })
    return item


@pytest.fixture
def cell_line_3(cell_line):
    item = cell_line.copy()
    item.update({
        'schema_version': '3',
        'aliases': [],
        'donors': [],
        'dbxrefs': [],
        'collections': [],
        'alternate_accessions': [],
        'treatments': []
    })
    return item
