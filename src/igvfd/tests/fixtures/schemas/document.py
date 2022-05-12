import pytest
from ...constants import *


@pytest.fixture
def experimental_protocol_document(testapp, other_lab, award):
    item = {
        'document_type': 'experimental protocol',
        'description': 'Generic experimental protocol',
        'award': award['@id'],
        'lab': other_lab['@id'],
        'attachment': {'download': 'red-dot.png', 'href': RED_DOT},
    }
    return testapp.post_json('/document', item).json['@graph'][0]
