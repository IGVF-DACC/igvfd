import pytest


@pytest.fixture
def measurement_set(testapp, lab, award, assay_term_starr):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'assay_term': assay_term_starr['@id']
    }
    return testapp.post_json('/measurement_set', item).json['@graph'][0]


@pytest.fixture
def measurement_set_v1(measurement_set, document_v1):
    item = measurement_set.copy()
    item.update({
        'schema_version': '1',
        'aliases': ['igvf:curated_set_v1'],
        'alternate_accessions': ['IGVFFS123BBB'],
        'collections': ['ENCODE'],
        'documents': [document_v1['@id']]
    })
    return item
