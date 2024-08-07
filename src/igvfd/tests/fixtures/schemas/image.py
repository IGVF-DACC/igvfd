import pytest
from ...constants import *


@pytest.fixture
def image(testapp):
    item = {
        'caption': 'red dot',
        'attachment': {'download': 'red-dot.png', 'href': RED_DOT},
    }
    return testapp.post_json('/image', item, status=201).json['@graph'][0]
