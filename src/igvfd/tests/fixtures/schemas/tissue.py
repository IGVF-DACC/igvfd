import pytest


@pytest.fixture
def tissue(testapp, lab, source, award, human_donor):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Homo sapiens',
        'donors': human_donor['@id']
    }
    return testapp.post_json('/tissue', item, status=201).json['@graph'][0]
