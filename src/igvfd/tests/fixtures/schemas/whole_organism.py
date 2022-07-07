import pytest


@pytest.fixture
def whole_organism1(testapp, lab, source, award, human_donor):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Homo sapiens',
        'donors': human_donor['@id']
    }
    return testapp.post_json('/whole_organism', item, status=201).json['@graph'][0]
