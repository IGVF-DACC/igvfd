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
