import pytest


@pytest.fixture
def curated_set_genome(testapp, lab, award):
    item = {
        'file_set_type': 'genome',
        'award': award['@id'],
        'lab': lab['@id']
    }
    return testapp.post_json('/curated_set', item).json['@graph'][0]


@pytest.fixture
def curated_set_transcriptome(testapp, lab, award):
    item = {
        'file_set_type': 'transcriptome',
        'award': award['@id'],
        'lab': lab['@id']
    }
    return testapp.post_json('/curated_set', item).json['@graph'][0]


@pytest.fixture
def curated_set_v1(analysis_set_base, human_donor, in_vitro_cell_line):
    item = analysis_set_base.copy()
    item.update({
        'schema_version': '1',
        'sample': [in_vitro_cell_line['@id']],
        'donor': [human_donor['@id']]
    })
    return item


@pytest.fixture
def curated_set_v2(curated_set_genome):
    item = curated_set_genome.copy()
    item.update({
        'schema_version': '1',
        'accession': 'IGVFFS000ZZZ'
    })
    return item


@pytest.fixture
def curated_set_v3(curated_set_genome):
    item = curated_set_genome.copy()
    item.update({
        'schema_version': '3',
        'references': ['10.1101/2023.08.02']
    })
    return item


@pytest.fixture
def curated_set_v4(lab, award):
    item = {
        'curated_set_type': 'genome',
        'award': award['@id'],
        'lab': lab['@id'],
        'schema_version': '4'
    }
    return item
