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


@pytest.fixture
def document_v1(experimental_protocol_document):
    item = experimental_protocol_document.copy()
    item.update({
        'schema_version': '1',
        'urls': [],
        'aliases': []
    })
    return item


@pytest.fixture
def plasmid_map_document(testapp, other_lab, award):
    item = {
        'document_type': 'plasmid map',
        'description': 'Generic experimental protocol',
        'award': award['@id'],
        'lab': other_lab['@id'],
        'attachment': {'download': 'red-dot.png', 'href': RED_DOT}
    }
    return testapp.post_json('/document', item).json['@graph'][0]
