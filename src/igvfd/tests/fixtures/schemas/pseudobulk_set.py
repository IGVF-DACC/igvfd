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
        'cell_annotation': sample_term_endothelial_cell['@id']
    }
    return testapp.post_json('/pseudobulk_set', item, status=201).json['@graph'][0]
