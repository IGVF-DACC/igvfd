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
        'schema_version': '2',
        'notes': 'Test.'
    })
    return item
