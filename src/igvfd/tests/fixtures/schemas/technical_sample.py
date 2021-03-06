import pytest


@pytest.fixture
def technical_sample_1(testapp, other_lab, award, source):
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'source': source['@id'],
        'sample_material': 'synthetic'
    }
    return testapp.post_json('/technical_sample', item, status=201).json['@graph'][0]


@pytest.fixture
def technical_sample_version_1(tissue):
    item = tissue.copy()
    item.update({
        'schema_version': '1',
        'dbxrefs': [],
        'aliases': [],
        'alternate_accessions': []
    })
    return item
