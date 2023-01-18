import pytest


@pytest.fixture
def analysis_set_base(
    testapp,
    award,
    lab
):
    item = {
        'award': award['@id'],
        'lab': lab['@id']
    }
    return testapp.post_json('/analysis_set', item, status=201).json['@graph'][0]


@pytest.fixture
def analysis_set_with_sample(
    testapp,
    award,
    lab,
    cell_line,
    analysis_set_base
):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'sample': [cell_line['@id']],
        'input_file_sets': [analysis_set_base['@id']]
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
        'donor': [human_donor['@id']],
        'input_file_sets': [analysis_set_base['@id']]
    }
    return testapp.post_json('/analysis_set', item, status=201).json['@graph'][0]
