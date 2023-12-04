import pytest


@pytest.fixture
def analysis_set_base(
    testapp,
    award,
    lab
):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'file_set_type': 'intermediate analysis'
    }
    return testapp.post_json('/analysis_set', item, status=201).json['@graph'][0]


@pytest.fixture
def analysis_set_with_sample(
    testapp,
    award,
    lab,
    in_vitro_cell_line,
    analysis_set_base
):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'samples': [in_vitro_cell_line['@id']],
        'input_file_sets': [analysis_set_base['@id']],
        'file_set_type': 'intermediate analysis'
    }
    return testapp.post_json('/analysis_set', item, status=201).json['@graph'][0]


@pytest.fixture
def analysis_set_with_donor(
    testapp,
    award,
    lab,
    human_donor,
    analysis_set_base
):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'donors': [human_donor['@id']],
        'input_file_sets': [analysis_set_base['@id']],
        'file_set_type': 'intermediate analysis'
    }
    return testapp.post_json('/analysis_set', item, status=201).json['@graph'][0]


@pytest.fixture
def analysis_set_v1(analysis_set_base, curated_set_genome, human_donor, in_vitro_cell_line):
    item = analysis_set_base.copy()
    item.update({
        'schema_version': '1',
        'sample': [in_vitro_cell_line['@id']],
        'donor': [human_donor['@id']],
        'input_file_set': [curated_set_genome['@id']]
    })
    return item


@pytest.fixture
def analysis_set_v3(award, lab):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'schema_version': '3'
    }
    return item


@pytest.fixture
def analysis_set_v4(analysis_set_v3):
    item = analysis_set_v3.copy()
    item.update({
        'schema_version': '4',
        'file_set_type': 'itermediate analysis',
        'description': ''
    })
    return item
