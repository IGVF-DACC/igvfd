import pytest


@pytest.fixture
def differentiated_tissue(testapp, lab, award, source, human_donor):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Homo sapiens',
        'donors': [human_donor['@id']]
    }
    return testapp.post_json('/differentiated_tissue', item, status=201).json['@graph'][0]


@pytest.fixture
def differentiated_tissue_1(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '1'
    })
    return item


@pytest.fixture
def differentiated_tissue_part_of(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'aliases': 'igvf-dacc:differentiated_tissue_part_of',
        'schema_version': '2',
        'collections': []
    })
    return item


@pytest.fixture
def differentiated_tissue_2(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '2'
    })
    return item


@pytest.fixture
def differentiated_tissue_3(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '3',
        'collections': []
    })
    return item


@pytest.fixture
def differentiated_tissue_4(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '4',
        'post_differentiation_time': 10,
        'post_differentiation_time_units': 'stage'
    })
    return item


@pytest.fixture
def differentiated_tissue_4_good_value(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '4',
        'post_differentiation_time': 7,
        'post_differentiation_time_units': 'month'
    })
    return item


@pytest.fixture
def differentiated_tissue_4_with_note(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '4',
        'post_differentiation_time': 10,
        'post_differentiation_time_units': 'stage',
        'notes': 'This is a note.'
    })
    return item
