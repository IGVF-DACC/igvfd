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
