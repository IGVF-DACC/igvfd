import pytest


@pytest.fixture
def pseudobulk_set_base(
    testapp,
    award,
    lab,
    tissue,
    sample_term_endothelial_cell
):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'file_set_type': 'pseudobulk analysis',
        'samples': [tissue['@id']],
        'cell_type': sample_term_endothelial_cell['@id']
    }
    return testapp.post_json('/pseudobulk_set', item, status=201).json['@graph'][0]


@pytest.fixture
def pseudobulk_set_2(
    testapp,
    award,
    lab,
    tissue,
    sample_term_pluripotent_stem_cell
):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'file_set_type': 'pseudobulk analysis',
        'samples': [tissue['@id']],
        'cell_type': sample_term_pluripotent_stem_cell['@id']
    }
    return testapp.post_json('/pseudobulk_set', item, status=201).json['@graph'][0]


@pytest.fixture
def pseudobulk_set_merged(
    testapp,
    award,
    lab,
    tissue,
    sample_term_endothelial_cell,
    pseudobulk_set_base,
    pseudobulk_set_2
):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'input_file_sets': [pseudobulk_set_base['@id'], pseudobulk_set_2['@id']],
        'merged': True,
        'file_set_type': 'pseudobulk analysis',
        'samples': [tissue['@id']],
        'cell_type': sample_term_endothelial_cell['@id']
    }
    return testapp.post_json('/pseudobulk_set', item, status=201).json['@graph'][0]
