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


@pytest.fixture
def status(testapp):
    url = '/test-igvf-items/'
    items_with_status = items.copy()
    for item in items_with_status:
        item['status'] = 'in progress'
        testapp.post_json(url, item)


def test_item_summary_property(testapp, content, root):
    res = testapp.get('/test-igvf-items/')
    igvf_item_uuid = res.json['@graph'][0]['uuid']
    igvf_item_id = res.json['@graph'][0]['@id']

    igvf_item = root.get_by_uuid(igvf_item_uuid)
    igvf_item_properties = igvf_item.properties
    igvf_item.update(igvf_item_properties)

    res = testapp.get(igvf_item_id)
    igvf_item_accession = res.json['accession']
    igvf_item_summary = res.json['summary']
    assert igvf_item_accession == igvf_item_summary


def test_item_status_update(testapp, status, root, dummy_request):
    res = testapp.get('/test-igvf-items/')  # returns a list of items
    # Get the UUID and ID of the first item
    igvf_item_uuid = res.json['@graph'][0]['uuid']
    igvf_item_id = res.json['@graph'][0]['@id']

    # Get the item from the root using the UUID
    igvf_item = root.get_by_uuid(igvf_item_uuid)
    # Get the current properties
    igvf_item_properties = igvf_item.properties
    igvf_item.update(igvf_item_properties)

    # When in progress, no release or preview timestamp
    res = testapp.get(igvf_item_id)
    assert res.json['status'] == 'in progress'
    assert 'preview_timestamp' not in res.json.keys()
    assert 'release_timestamp' not in res.json.keys()

    # Update the item to 'preview' status, should have a preview timestamp
    igvf_item.set_status('preview', dummy_request)

    res = testapp.get(igvf_item_id)
    assert res.json['status'] == 'preview'
    assert 'preview_timestamp' in res.json.keys()

    # Update the item to 'released' status
    igvf_item.set_status('released', dummy_request)
    res = testapp.get(igvf_item_id)
    assert res.json['status'] == 'released'
    assert 'release_timestamp' in res.json.keys()
