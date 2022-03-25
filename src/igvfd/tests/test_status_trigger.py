import pytest

from datetime import datetime
from pyramid.httpexceptions import HTTPNotFound


items = [
    {'description': 'item0'},
    {'description': 'item1'},
    {'description': 'item2'},
]


@pytest.fixture
def content(testapp):
    url = '/test-igvf-items/'
    for item in items:
        testapp.post_json(url, item)


def test_item_set_status_method_exists(testapp, content, root):
    res = testapp.get('/test-igvf-items/')
    igvf_item_uuid = res.json['@graph'][0]['uuid']
    igvf_item = root.get_by_uuid(igvf_item_uuid)
    set_status_method = getattr(igvf_item, 'set_status', None)
    assert callable(set_status_method)


def test_item_set_status_up_down_lists_exists(testapp, content, root):
    res = testapp.get('/test-igvf-items/')
    igvf_item_uuid = res.json['@graph'][0]['uuid']
    igvf_item = root.get_by_uuid(igvf_item_uuid)
    assert hasattr(igvf_item, 'set_status_up')
    assert hasattr(igvf_item, 'set_status_down')
    assert isinstance(igvf_item.set_status_up, list)
    assert isinstance(igvf_item.set_status_down, list)


def test_item_set_status_no_status_validation_error(testapp, content, root):
    res = testapp.get('/test-igvf-items/')
    igvf_item_uuid = res.json['@graph'][0]['uuid']
    igvf_item_id = res.json['@graph'][0]['@id']
    igvf_item = root.get_by_uuid(igvf_item_uuid)
    igvf_item_properties = igvf_item.properties
    igvf_item_properties.pop('status')
    igvf_item.update(igvf_item_properties)
    res = testapp.get(igvf_item_id)
    assert 'status' not in res.json
    res = testapp.patch_json(igvf_item_id + '@@set_status', {'status': 'released'}, status=422)
    assert res.json['errors'][0]['description'] == 'No property status'


def test_item_set_status_invalid_transition_parent(testapp, content, root, dummy_request):
    # Can't go from deleted to released.
    from snovault.validation import ValidationFailure
    res = testapp.get('/test-igvf-items/')
    igvf_item_uuid = res.json['@graph'][0]['uuid']
    igvf_item_id = res.json['@graph'][0]['@id']
    testapp.patch_json(igvf_item_id, {'status': 'deleted'}, status=200)
    igvf_item = root.get_by_uuid(igvf_item_uuid)
    with pytest.raises(ValidationFailure) as e:
        igvf_item.set_status('released', dummy_request)
    assert e.value.detail['description'] == 'Status transition deleted to released not allowed'


def test_item_set_status_invalid_transition_child(testapp, content, root, dummy_request):
    # Don't raise error if invalid transition on child object.
    res = testapp.get('/test-igvf-items/')
    igvf_item_uuid = res.json['@graph'][0]['uuid']
    igvf_item_id = res.json['@graph'][0]['@id']
    testapp.patch_json(igvf_item_id, {'status': 'deleted'}, status=200)
    igvf_item = root.get_by_uuid(igvf_item_uuid)
    assert igvf_item.set_status('released', dummy_request, parent=False) is False


def test_item_release_endpoint_calls_set_status(testapp, content, mocker):
    from igvfd.types.base import Item
    res = testapp.get('/test-igvf-items/')
    igvf_item_id = res.json['@graph'][0]['@id']
    mocker.patch('igvfd.types.base.Item.set_status')
    testapp.patch_json(igvf_item_id + '@@set_status', {'status': 'released'})
    assert Item.set_status.call_count == 1


def test_item_release_endpoint_triggers_set_status(testapp, content, mocker):
    from igvfd.types.base import Item
    res = testapp.get('/test-igvf-items/')
    igvf_item_id = res.json['@graph'][0]['@id']
    mocker.spy(Item, 'set_status')
    testapp.patch_json(igvf_item_id + '@@set_status', {'status': 'released'})
    assert Item.set_status.call_count == 1


def test_set_status_endpoint_status_not_specified(testapp, content):
    res = testapp.get('/test-igvf-items/')
    igvf_item_id = res.json['@graph'][0]['@id']
    res = testapp.patch_json(igvf_item_id + '@@set_status?update=true', {}, status=422)
    assert res.json['errors'][0]['description'] == 'Status not specified'


def test_set_status_endpoint_status_specified(testapp, content):
    res = testapp.get('/test-igvf-items/')
    igvf_item_id = res.json['@graph'][0]['@id']
    testapp.patch_json(
        igvf_item_id + '@@set_status?update=true&force_audit=true',
        {'status': 'released'},
        status=200
    )
