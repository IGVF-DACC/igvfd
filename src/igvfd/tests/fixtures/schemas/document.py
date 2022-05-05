import pytest


@pytest.fixture
def experimental_protocol_document(testapp, other_lab, award):
    item = {
        'document_type': 'experimental protocol',
        'description': 'Generic experimental protocol',
        'award': award['@id'],
        'lab': other_lab['@id'],
        'attachment': {'download': 'Antibody_Characterization_IGVF.pdf', 'href': Antibody_Characterization_IGVF.pdf},
    }
    return testapp.post_json('/document', item).json['@graph'][0]
