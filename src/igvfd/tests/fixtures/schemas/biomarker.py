import pytest


@pytest.fixture
def biomarker_absent(testapp):
    item = {
        'name': 'CD243',
        'quantification': '-',
        'biomarker_type': 'cell-surface',
        'synonyms': ['ABC20', 'CD243', 'CLCS', 'GP170', 'MDR1', 'P-gp', 'PGY1']
    }
    return testapp.post_json('/biomarker', item, status=201).json['@graph'][0]


@pytest.fixture
def biomarker_high(testapp):
    item = {
        'name': 'CD243',
        'quantification': 'high',
        'biomarker_type': 'cell-surface',
        'synonyms': ['ABC20', 'CD243', 'CLCS', 'GP170', 'MDR1', 'P-gp', 'PGY1']
    }
    return testapp.post_json('/biomarker', item, status=201).json['@graph'][0]
