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


def test_item_summary_property(testapp, content):
    res = testapp.get('/test-igvf-items/')
    igvf_item_uuid = res.json['@graph'][0]['uuid']
    igvf_item_summary = res.json['@graph'][0]['summary']
    assert igvf_item_uuid == igvf_item_summary
