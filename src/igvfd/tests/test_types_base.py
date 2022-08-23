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
