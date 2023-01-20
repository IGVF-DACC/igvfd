import pytest


@pytest.fixture
def curated_set_genome(testapp, lab, award):
    item = {
        'curated_set_type': 'genome',
        'award': award['@id'],
        'lab': lab['@id']
    }
    return testapp.post_json('/curated_set', item).json['@graph'][0]


@pytest.fixture
def curated_set_v1(analysis_set_base, human_donor, cell_line):
    item = analysis_set_base.copy()
    item.update({
        'schema_version': '1',
        'sample': [cell_line['@id']],
        'donor': [human_donor['@id']]
    })
    return item


@pytest.fixture
def curated_set_v2(curated_set_genome):
    item = curated_set_genome.copy()
    item.update({
        'schema_version': '1'
    })
    return item
