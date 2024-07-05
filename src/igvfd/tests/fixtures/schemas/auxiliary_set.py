import pytest


@pytest.fixture
def base_auxiliary_set(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'file_set_type': 'gRNA sequencing'
    }
    return testapp.post_json('/auxiliary_set', item).json['@graph'][0]


@pytest.fixture
def auxiliary_set_cell_sorting(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'file_set_type': 'cell sorting'
    }
    return testapp.post_json('/auxiliary_set', item).json['@graph'][0]


@pytest.fixture
def auxiliary_set_v1(base_auxiliary_set):
    item = base_auxiliary_set.copy()
    item.update({
        'schema_version': '1',
        'references': ['10.1101/2023.08.02']
    })
    return item


@pytest.fixture
def auxiliary_set_v2(lab, award):
    item = {
        'schema_version': '2',
        'award': award['@id'],
        'lab': lab['@id'],
        'auxiliary_type': 'gRNA sequencing'
    }
    return item


@pytest.fixture
def auxiliary_set_v3(base_auxiliary_set):
    item = base_auxiliary_set.copy()
    item.update({
        'schema_version': '3',
        'moi': 1,
        'construct_libraries': 'TSTDSobject',
        'notes': 'Previous note.'
    })
    return item


@pytest.fixture
def auxiliary_set_v4(auxiliary_set_v3):
    item = auxiliary_set_v3.copy()
    item.update({
        'schema_version': '4',
        'description': ''
    })
    return item


@pytest.fixture
def auxiliary_set_v5(auxiliary_set_v4):
    item = auxiliary_set_v4.copy()
    item.update({
        'schema_version': '5',
        'file_set_type': 'oligo-conjugated antibodies'
    })
    return item


@pytest.fixture
def auxiliary_set_v7_circularized_barcode(base_auxiliary_set):
    item = base_auxiliary_set.copy()
    item.update({
        'schema_version': '7',
        'file_set_type': 'circularized barcode detection'
    })
    return item


@pytest.fixture
def auxiliary_set_v7_barcode_seq(base_auxiliary_set):
    item = base_auxiliary_set.copy()
    item.update({
        'schema_version': '7',
        'file_set_type': 'quantification barcode sequencing'
    })
    return item
