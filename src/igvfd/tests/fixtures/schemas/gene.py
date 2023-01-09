import pytest


@pytest.fixture
def gene_myc_hs(testapp):
    item = {
        'dbxref': [
            'HGNC:7553'
        ],
        'geneid': 'ENSG00000136997',
        'symbol': 'MYC',
        'taxa': 'Homo sapiens'
    }
    return testapp.post_json('/gene', item, status=201).json['@graph'][0]


@pytest.fixture
def gene_zscan10_mm(testapp):
    item = {
        'dbxref': [
            'Vega:OTTMUSG00000029797',
            'UniProtKB:Q3URR7',
            'RefSeq:NM_001033425.3',
            'RefSeq:NM_001033425.4',
            'MGI:3040700'
        ],
        'geneid': 'ENSMUSG00000023902',
        'symbol': 'Zcan10',
        'taxa': 'Mus musculus'
    }
    return testapp.post_json('/gene', item, status=201).json['@graph'][0]


@pytest.fixture
def gene_v1(gene_zscan10_mm):
    item = gene_zscan10_mm.copy()
    item.update({
        'schema_version': '1',
        'aliases': []
    })
    return item


@pytest.fixture
def gene_v2(gene_zscan10_mm):
    item = gene_zscan10_mm.copy()
    item.update({
        'schema_version': '2',
        'aliases': []
    })
    return item


@pytest.fixture
def gene_CD1E(testapp):
    item = {
        'dbxref': [
            'HGNC:1638'
        ],
        'geneid': 'ENSG00000158488',
        'symbol': 'CD1E',
        'taxa': 'Homo sapiens'
    }
    return testapp.post_json('/gene', item, status=201).json['@graph'][0]


@pytest.fixture
def gene_v3(gene_zscan10_mm):
    item = gene_zscan10_mm.copy()
    item.update({
        'schema_version': '3',
        'aliases': ['igvf:gene_v3'],
        'synonyms': ['UCHL3'],
        'locations':
        {
            'assembly': 'GRCh38',
            'chromosome': 'chr3',
            'start': 52401004,
            'end': 52410030
        },
        'dbxrefs': ['UniProtKB:F8W6N4']
    })
    return item
