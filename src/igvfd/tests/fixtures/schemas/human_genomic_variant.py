import pytest


@pytest.fixture
def human_genomic_variant(testapp):
    item = {
        'ref': 'A',
        'alt': 'G',
        'chromosome': 'chr1',
        'assembly': 'GRCh38',
        'position': 1000000,
        'rsid': 'rs100',
        'refseq_id': 'NC_999999.00'
    }
    return testapp.post_json('/human_genomic_variant', item, status=201).json['@graph'][0]
