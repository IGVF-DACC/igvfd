import pytest


@pytest.fixture
def gene_myc_hs(testapp):
    item = {
        'dbxrefs': [
            'HGNC:7553'
        ],
        'geneid': '4609',
        'symbol': 'MYC',
        'ncbi_entrez_status': 'live',
        'organism': 'Homo sapiens'
    }
    return testapp.post_json('/gene', item, status=201).json['@graph'][0]


@pytest.fixture
def gene_zscan10_mm(testapp):
    item = {
        'dbxrefs': [
            'Vega:OTTMUSG00000029797',
            'UniProtKB:Q3URR7',
            'ENSEMBL:ENSMUSG00000023902',
            'RefSeq:NM_001033425.3',
            'RefSeq:NM_001033425.4',
            'MGI:3040700'
        ],
        'geneid': '332221',
        'symbol': 'Zcan10',
        'ncbi_entrez_status': 'live',
        'organism': 'Mus musculus'
    }
    return testapp.post_json('/gene', item, status=201).json['@graph'][0]
