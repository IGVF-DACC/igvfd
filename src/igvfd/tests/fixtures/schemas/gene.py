import pytest


@pytest.fixture
def gene_myc_hs(testapp):
    item = {
        'dbxrefs': ['HGNC:7553'],
        'geneid': '4609',
        'symbol': 'MYC',
        'ncbi_entrez_status': 'live',
        'organism': 'Homo sapiens'
    }
    return testapp.post_json('/gene', item, status=201).json['@graph'][0]
