import pytest


@pytest.fixture
def other_lab(testapp, verified_member):
    item = {
        'name': 'other-lab',
        'institute_label': 'Other Institute',
        'pi': verified_member['@id'],
    }
    return testapp.post_json('/lab', item, status=201).json['@graph'][0]


@pytest.fixture
def fake_lab(unverified_member):
    return{
        'name': 'Fake Lab',
        'institute_label': 'Fake Institute',
        'pi': unverified_member['@id'],
    }


@pytest.fixture
def lab_1_0(fake_lab):
    item = fake_lab.copy()
    item.update({
        'schema_version': '1',
        'status': 'CURRENT',
    })
    return item


@pytest.fixture
def lab(testapp, pi):
    item = {
        'name': 'igvf-lab',
        'institute_label': 'Stanford',
        'pi': pi['@id'],
    }
    return testapp.post_json('/lab', item).json['@graph'][0]


@pytest.fixture
def lab_1(lab):
    item = lab.copy()
    item.update({
        'schema_version': '1',
        'awards': [],
        'aliases': []
    })
    return item
