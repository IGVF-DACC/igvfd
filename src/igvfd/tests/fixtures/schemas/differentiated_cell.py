import pytest


@pytest.fixture
def differentiated_cell(testapp, lab, award, source, human_donor, sample_term_K562):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Homo sapiens',
        'donors': [human_donor['@id']],
        'biosample_term': sample_term_K562['@id']
    }
    return testapp.post_json('/differentiated_cell', item, status=201).json['@graph'][0]


@pytest.fixture
def differentiated_cell_v1(differentiated_cell):
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


@pytest.fixture
def differentiated_cell_v2(differentiated_cell):
    item = differentiated_cell.copy()
    item.update({
        'schema_version': '2'
    })
    return item


@pytest.fixture
def differentiated_cell_v3(differentiated_cell):
    item = differentiated_cell.copy()
    item.update({
        'schema_version': '3',
        'aliases': [],
        'donors': [],
        'dbxrefs': [],
        'collections': [],
        'alternate_accessions': [],
        'treatments': [],
        'differentiation_treatments': []
    })
    return item


@pytest.fixture
def differentiated_cell_v4(differentiated_cell, phenotype_term_alzheimers):
    item = differentiated_cell.copy()
    item.update({
        'schema_version': '4',
        'disease_term': phenotype_term_alzheimers['@id']
    })
    return item


@pytest.fixture
def differentiated_cell_v5(differentiated_cell):
    item = differentiated_cell.copy()
    item.update({
<<<<<<< HEAD
        'schema_version': '5',
        'age': '10',
        'age_units': 'day',
        'life_stage': 'embryonic'
    })
    return item


@pytest.fixture
def differentiated_cell_v5_unknown(differentiated_cell):
    item = differentiated_cell.copy()
    item.update({
        'schema_version': '5',
        'age': 'unknown',
        'life_stage': 'unknown'
    })
    return item


@pytest.fixture
def differentiated_cell_v5_90_or_above(differentiated_cell):
    item = differentiated_cell.copy()
    item.update({
        'schema_version': '5',
        'age': '90 or above',
        'age_units': 'year',
        'life_stage': 'adult'
=======
        'schema_version': '6'
>>>>>>> add tests, inserts, upgrades
    })
    return item
