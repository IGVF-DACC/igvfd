import pytest


@pytest.fixture
def human_donor(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Homo sapiens',
    }
    return testapp.post_json('/human_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def parent_human_donor_1(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Homo sapiens',
    }
    return testapp.post_json('/human_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def parent_human_donor_2(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Homo sapiens',
    }
    return testapp.post_json('/human_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def parent_human_donor_3(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Homo sapiens',
    }
    return testapp.post_json('/human_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def human_donor_orphan(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Homo sapiens',
    }
    return testapp.post_json('/human_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def human_male_donor(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Homo sapiens',
        'sex': 'male'
    }
    return testapp.post_json('/human_donor', item, status=201).json['@graph'][0]
