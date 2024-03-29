import pytest


@pytest.fixture
def biomarker_CD243_absent(testapp, lab, award):
    item = {
        'name': 'CD243',
        'quantification': 'negative',
        'classification': 'cell surface protein',
        'aliases': ['igvf:biomarker_CD243_absent'],
        'synonyms': ['ABC20', 'CD243', 'CLCS', 'GP170', 'MDR1', 'P-gp', 'PGY1'],
        'award': award['@id'],
        'lab': lab['@id']
    }
    return testapp.post_json('/biomarker', item, status=201).json['@graph'][0]


@pytest.fixture
def biomarker_CD243_high(testapp, lab, award):
    item = {
        'name': 'CD243',
        'quantification': 'high',
        'classification': 'cell surface protein',
        'aliases': ['igvf:biomarker_CD243_high'],
        'synonyms': ['ABC20', 'CD243', 'CLCS', 'GP170', 'MDR1', 'P-gp', 'PGY1'],
        'award': award['@id'],
        'lab': lab['@id']
    }
    return testapp.post_json('/biomarker', item, status=201).json['@graph'][0]


@pytest.fixture
def biomarker_CD1e_low(testapp, lab, award):
    item = {
        'name': 'CD1e',
        'quantification': 'low',
        'classification': 'cell surface protein',
        'synonyms': ['R2G1', 'HSCDIEL'],
        'award': award['@id'],
        'lab': lab['@id']
    }
    return testapp.post_json('/biomarker', item, status=201).json['@graph'][0]


@pytest.fixture
def biomarker_IgA_present(testapp, lab, award):
    item = {
        'name': 'IgA',
        'quantification': 'positive',
        'classification': 'cell surface protein',
        'award': award['@id'],
        'lab': lab['@id']
    }
    return testapp.post_json('/biomarker', item, status=201).json['@graph'][0]


@pytest.fixture
def biomarker_v1(biomarker_CD243_absent):
    item = biomarker_CD243_absent.copy()
    item.update({
        'schema_version': '1'
    })
    return item


@pytest.fixture
def biomarker_v2(biomarker_v1):
    item = biomarker_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item
