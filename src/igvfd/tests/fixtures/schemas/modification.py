import pytest


@pytest.fixture
def modification(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'cas': 'dCas9',
        'modality': 'interference',
        'cas_species': 'Streptococcus pyogenes (Sp)'
    }
    return testapp.post_json('/modification', item, status=201).json['@graph'][0]


@pytest.fixture
def modification_missing_cas_sp(modification):
    item = modification.copy()
    item.pop('cas_species', None)
    item.update({
        'schema_version': '1',
        'notes': 'Test.'
    })
    return item


@pytest.fixture
def modification_v2(modification, source):
    item = modification.copy()
    item.update({
        'schema_version': '2',
        'source': source['@id']
    })
    return item


@pytest.fixture
def modification_activation(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'cas': 'dCas9',
        'modality': 'activation',
        'cas_species': 'Streptococcus pyogenes (Sp)'
    }
    return testapp.post_json('/modification', item, status=201).json['@graph'][0]


@pytest.fixture
def modification_v3(modification_activation):
    item = modification_activation.copy()
    item.update({
        'schema_version': '3',
        'description': ''
    })
    return item
