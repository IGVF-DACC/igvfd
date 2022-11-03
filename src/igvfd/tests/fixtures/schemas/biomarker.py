import pytest


@pytest.fixture
def biomarker_CD243_absent(testapp):
    item = {
        'name': 'CD243',
        'quantification': '-',
        'biomarker_type': 'cell-surface',
        'synonyms': ['ABC20', 'CD243', 'CLCS', 'GP170', 'MDR1', 'P-gp', 'PGY1']
    }
    return testapp.post_json('/biomarker', item, status=201).json['@graph'][0]


@pytest.fixture
def biomarker_CD243_high(testapp):
    item = {
        'name': 'CD243',
        'quantification': 'high',
        'biomarker_type': 'cell-surface',
        'synonyms': ['ABC20', 'CD243', 'CLCS', 'GP170', 'MDR1', 'P-gp', 'PGY1']
    }
    return testapp.post_json('/biomarker', item, status=201).json['@graph'][0]


@pytest.fixture
def biomarker_CD1e_low(testapp):
    item = {
        'name': 'CD1e',
        'quantification': 'low',
        'biomarker_type': 'cell-surface',
        'synonyms': ['R2G1', 'HSCDIEL']
    }
    return testapp.post_json('/biomarker', item, status=201).json['@graph'][0]


@pytest.fixture
def biomarker_IgA_present(testapp):
    item = {
        'name': 'IgA',
        'quantification': '+',
        'biomarker_type': 'cell-surface'
    }
    return testapp.post_json('/biomarker', item, status=201).json['@graph'][0]
