import pytest


@pytest.fixture
def other_lab(testapp):
    item = {
        'name': 'other-lab',
        'institute_label': 'Stanford',
        'pi': 'massa.porta@varius.mauris',
    }
    return testapp.post_json('/lab', item, status=201).json['@graph'][0]


@pytest.fixture
def lab_0_0():
    return{
        'name': 'Fake Lab',
        'institute_label': 'Fake Institute',
        'pi': 'massa.porta@varius.mauris',
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
def lab(testapp):
    item = {
        'name': 'igvf-lab',
        'institute_label': 'Stanford',
        'pi': 'massa.porta@varius.mauris',
    }
    return testapp.post_json('/lab', item).json['@graph'][0]
