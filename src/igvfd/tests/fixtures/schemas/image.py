import pytest
from ...constants import *


@pytest.fixture
def image(testapp):
    item = {
        'attachment': {'download': 'red-dot.png', 'href': RED_DOT},
        'release_timestamp': '2024-03-06T12:34:56Z',
        'status': 'released'
    }
    return testapp.post_json('/image', item, status=201).json['@graph'][0]
