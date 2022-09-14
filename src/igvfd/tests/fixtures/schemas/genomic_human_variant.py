import pytest


@pytest.fixture
def genomic_human_variant(testapp):
    item = {
        'ref': 'A',
        'alt': 'G',
        'chromosome': 'chr1',
        'assembly': 'GRCh38',
        'position': 1000000,
        'rsid': 'rs100',
        'refseq_sequence_id': 'NT_999.00'
    }
    return testapp.post_json('/genomic_human_variant', item, status=201).json['@graph'][0]
