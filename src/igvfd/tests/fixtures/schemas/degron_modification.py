import pytest


@pytest.fixture
def degron_modification(testapp, lab, award, gene_myc_hs):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'degron_system': 'dCas9',
        'tagged_proteins': [gene_myc_hs['@id']]
    }
    return testapp.post_json('/degron_modification', item, status=201).json['@graph'][0]
