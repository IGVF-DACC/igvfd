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


@pytest.fixture
def human_genomic_variant_no_refseq_id(testapp):
    item = {
        'ref': 'A',
        'alt': 'G',
        'chromosome': 'chr1',
        'assembly': 'GRCh38',
        'position': 1000000,
        'rsid': 'rs100',
        'reference_sequence': 'ACTGAGGA'
    }
    return testapp.post_json('/human_genomic_variant', item, status=201).json['@graph'][0]


@pytest.fixture
def human_genomic_variant_v1(human_genomic_variant):
    item = human_genomic_variant.copy()
    item.update({
        'schema_version': '1',
        'refseq_id': 'NC_999999i00'
    })
    return item


@pytest.fixture
def human_genomic_variant_match(testapp):
    item = {
        'ref': 'A',
        'alt': 'A',
        'chromosome': 'chr1',
        'assembly': 'GRCh38',
        'position': 1000000,
        'rsid': 'rs100',
        'refseq_id': 'NC_999999.00'
    }
    return testapp.post_json('/human_genomic_variant', item, status=201).json['@graph'][0]


@pytest.fixture
def human_genomic_variant_v2(human_genomic_variant_v1):
    item = human_genomic_variant_v1.copy()
    item.update({
        'schema_version': '1',
        'description': ''
    })
    return item
