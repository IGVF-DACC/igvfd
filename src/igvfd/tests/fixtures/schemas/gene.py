import pytest


@pytest.fixture
def gene_myc_hs(testapp):
    item = {
        'dbxrefs': [
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
        'dbxrefs': [
            'Vega:OTTMUSG00000029797',
            'UniProtKB:Q3URR7',
            'RefSeq:NM_001033425.3',
            'RefSeq:NM_001033425.4',
            'MGI:3040700'
        ],
        'geneid': 'ENSEMBL:ENSMUSG00000023902',
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
