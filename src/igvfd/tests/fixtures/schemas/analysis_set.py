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
def principal_analysis_set(
    testapp,
    award,
    lab,
    analysis_set_base
):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'input_file_sets': [analysis_set_base['@id']],
        'file_set_type': 'principal analysis'
    }
    return testapp.post_json('/analysis_set', item, status=201).json['@graph'][0]


@pytest.fixture
def intermediate_analysis_set(
    testapp,
    award,
    lab,
    analysis_set_base
):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'input_file_sets': [analysis_set_base['@id']],
        'file_set_type': 'intermediate analysis'
    }
    return testapp.post_json('/analysis_set', item, status=201).json['@graph'][0]


@pytest.fixture
def principal_analysis_set(
    testapp,
    award,
    lab,
    measurement_set
):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'input_file_sets': [measurement_set['@id']],
        'file_set_type': 'principal analysis'
    }
    return testapp.post_json('/analysis_set', item, status=201).json['@graph'][0]


@pytest.fixture
def analysis_set_with_workflow(
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
        'description': ''
    })
    return item


@pytest.fixture
def analysis_set_v6(analysis_set_v4):
    item = analysis_set_v4.copy()
    item.update({
        'schema_version': '6',
        'file_set_type': 'primary analysis'
    })
    return item


@pytest.fixture
def analysis_set_v7(analysis_set_base):
    item = analysis_set_base.copy()
    item.update({
        'schema_version': '7',
        'publication_identifiers': ['doi:10.1016/j.molcel.2021.05.020']
    })
    return item
