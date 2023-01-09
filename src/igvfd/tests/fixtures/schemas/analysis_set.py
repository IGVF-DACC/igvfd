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
        'input_file_set': [analysis_set_base['@id']]
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
        'input_file_set': [analysis_set_base['@id']]
    }
    return testapp.post_json('/analysis_set', item, status=201).json['@graph'][0]


@pytest.fixture
def analysis_set_v1(analysis_set_base, document_v1):
    item = analysis_set_base.copy()
    item.update({
        'schema_version': '1',
        'aliases': ['igvf:analysis_set_v1'],
        'alternate_accessions': ['IGVFFS123AAA'],
        'collections': ['ENCODE'],
        'documents': [document_v1['@id']]
    })
    return item
