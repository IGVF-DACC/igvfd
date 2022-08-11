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
def differentiated_tissue_v1(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '1'
    })
    return item


@pytest.fixture
def differentiated_tissue_part_of(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'aliases': 'igvf-dacc:differentiated_tissue_part_of'
    })
    return item


@pytest.fixture
def differentiated_tissue_v2(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '2'
    })
    return item


@pytest.fixture
def differentiated_tissue_v3(differentiated_tissue):
    item = differentiated_tissue.copy()
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
def differentiated_tissue_v4(differentiated_tissue, phenotype_term_alzheimers):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '4',
        'disease_term': phenotype_term_alzheimers['@id']
    })
    return item


@pytest.fixture
def differentiated_tissue_v5(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '5',
        'post_differentiation_time': 10,
        'post_differentiation_time_units': 'stage'
    })
    return item


@pytest.fixture
def differentiated_tissue_v5_good_value(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '5',
        'post_differentiation_time': 7,
        'post_differentiation_time_units': 'month'
    })
    return item


@pytest.fixture
def differentiated_tissue_v5_with_note(differentiated_tissue):
    item = differentiated_tissue.copy()
    item.update({
        'schema_version': '5',
        'post_differentiation_time': 10,
        'post_differentiation_time_units': 'stage',
        'notes': 'This is a note.'
    })
    return item
