import pytest
from ...constants import *


@pytest.fixture
def image(testapp):
    item = {
        'attachment': {'download': 'red-dot.png', 'href': RED_DOT},
        'uuid': 'b69a3fed-f708-4f29-b7be-0e83c0ba58a9',
    }
    return testapp.post_json('/image', item, status=201).json['@graph'][0]
