import pytest


@pytest.fixture
def cell_line(testapp, other_lab, award, human_donor):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'source': other_lab['@id'],
        'taxa': 'Homo sapiens',
        'donors': human_donor['@id']
    }
    return testapp.post_json('/cell_line', item, status=201).json['@graph'][0]


@pytest.fixture
def cell_line_with_date_obtained(testapp, other_lab, award, human_donor):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'source': other_lab['@id'],
        'date_obtained': '2022-04-02',
        'taxa': 'Homo sapiens',
        'donors': human_donor['@id']
    }
    return testapp.post_json('/cell_line', item, status=201).json['@graph'][0]
