import pytest


@pytest.fixture
def primary_cell(testapp, other_lab, award, human_donor):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'source': other_lab['@id'],
        'taxa': 'Homo sapiens',
        'donors': [human_donor['@id']]
    }
    return testapp.post_json('/primary_cell', item, status=201).json['@graph'][0]


@pytest.fixture
def pooled_from_primary_cell(testapp, lab, award, source, human_donor):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Homo sapiens',
        'donors': [human_donor['@id']]
    }
    return testapp.post_json('/primary_cell', item, status=201).json['@graph'][0]


@pytest.fixture
def pooled_from_primary_cell_2(testapp, lab, award, source, human_donor):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Homo sapiens',
        'donors': [human_donor['@id']]
    }
    return testapp.post_json('/primary_cell', item, status=201).json['@graph'][0]


@pytest.fixture
def primary_cell_v1(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '1'
    })
    return item


@pytest.fixture
def primary_cell_part_of(primary_cell):
    item = primary_cell.copy()
    item.update({
        'aliases': 'igvf-dacc:primary_cell_part_of'
    })
    return item


@pytest.fixture
def primary_cell_v2(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '2'
    })
    return item


@pytest.fixture
def primary_cell_v3(primary_cell):
    item = primary_cell.copy()
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


@pytest.fixture
<<<<<<< HEAD
def primary_cell_v4(primary_cell, phenotype_term_alzheimers):
    item = primary_cell.copy()
    item.update({
        'schema_version': '4',
        'disease_term': phenotype_term_alzheimers['@id']
=======
def primary_cell_v4(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '4',
        'age': '10',
        'age_units': 'day',
        'life_stage': 'postnatal'
    })
    return item


@pytest.fixture
def primary_cell_v4_unknown(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '4',
        'age': 'unknown',
        'life_stage': 'unknown'
    })
    return item


@pytest.fixture
def primary_cell_v4_90_or_above(primary_cell):
    item = primary_cell.copy()
    item.update({
        'schema_version': '4',
        'age': '90 or above',
        'age_units': 'year',
        'life_stage': 'adult'
>>>>>>> 932a539 (tests, upgrade tests, inserts fixed, fixtures added)
    })
    return item
