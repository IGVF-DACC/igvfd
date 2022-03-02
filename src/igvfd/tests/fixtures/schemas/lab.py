import pytest


@pytest.fixture
def other_lab(testapp, submitter):
    item = {
        'name': 'other-lab',
        'institute_label': 'Stanford',
        'pi': submitter['@id'],
    }
    return testapp.post_json('/lab', item, status=201).json['@graph'][0]


@pytest.fixture
def lab_0_0(submitter):
    return{
        'name': 'Fake Lab',
        'institute_label': 'Fake Institute',
        'pi': submitter['@id'],
    }


@pytest.fixture
def lab_1_0(lab_0_0):
    item = lab_0_0.copy()
    item.update({
        'schema_version': '1',
        'status': 'CURRENT',
    })
    return item


@pytest.fixture
def lab(testapp, submitter):
    item = {
        'name': 'igvf-lab',
        'institute_label': 'Stanford',
        'pi': submitter['@id'],
    }
    return testapp.post_json('/lab', item).json['@graph'][0]
