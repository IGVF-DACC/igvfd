import pytest


@pytest.fixture
def curated_set_genome(testapp, lab, award):
    item = {
        'curated_set_type': 'genome',
        'award': award['@id'],
        'lab': lab['@id']
    }
    return testapp.post_json('/curated_set', item).json['@graph'][0]


@pytest.fixture
def curated_set_v1(curated_set_genome, document_v1):
    item = curated_set_genome.copy()
    item.update({
        'schema_version': '1',
        'aliases': ['igvf:curated_set_v1'],
        'alternate_accessions': ['IGVFFS123BBB'],
        'collections': ['ENCODE'],
        'documents': [document_v1['@id']],
        'references': ['doi:10.1101/gr.275819.122']
    })
    return item
