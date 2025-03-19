import pytest


@pytest.fixture
def gene_myc_hs(testapp):
    item = {
        'dbxrefs': [
            'HGNC:7553'
        ],
        'geneid': 'ENSG00000136997',
        'version_number': '7',
        'transcriptome_annotation': 'GENCODE 42',
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
        'geneid': 'ENSMUSG00000023902',
        'version_number': '3',
        'transcriptome_annotation': 'GENCODE M30',
        'symbol': 'Zcan10',
        'taxa': 'Mus musculus'
    }
    return testapp.post_json('/gene', item, status=201).json['@graph'][0]


@pytest.fixture
def gene_CRLF2_par_y(testapp):
    item = {
        'dbxrefs': [
            'HGNC:14281'
        ],
        'geneid': 'ENSG00000205755_PAR_Y',
        'version_number': '3',
        'transcriptome_annotation': 'GENCODE 42',
        'symbol': 'CRLF2',
        'taxa': 'Homo sapiens'
    }
    return testapp.post_json('/gene', item, status=201).json['@graph'][0]


@pytest.fixture
def gene_CD1E(testapp):
    item = {
        'dbxrefs': [
            'HGNC:1638'
        ],
        'geneid': 'ENSG00000158488',
        'version_number': '3',
        'transcriptome_annotation': 'GENCODE 42',
        'symbol': 'CD1E',
        'taxa': 'Homo sapiens'
    }
    return testapp.post_json('/gene', item, status=201).json['@graph'][0]


@pytest.fixture
def gene_TAB3_AS1(testapp):
    item = {
        'dbxrefs': [
            'ENTREZ:727682'
        ],
        'geneid': 'ENSG00000231542',
        'version_number': '1',
        'transcriptome_annotation': 'GENCODE 43',
        'symbol': 'TAB3-AS1',
        'taxa': 'Homo sapiens'
    }
    return testapp.post_json('/gene', item, status=201).json['@graph'][0]


@pytest.fixture
def gene_MAGOH2P(testapp):
    item = {
        'dbxrefs': [
            'HGNC:30148'
        ],
        'geneid': 'ENSG00000264176',
        'version_number': '1',
        'transcriptome_annotation': 'GENCODE 43',
        'symbol': 'MAGOH2P',
        'taxa': 'Homo sapiens'
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
def gene_v3(testapp):
    item = {
        'dbxrefs': [
            'MGI:97486'
        ],
        'geneid': 'ENSMUSG00000004231.8',
        'symbol': 'Pax2',
        'taxa': 'Mus musculus'
    }
    return item


@pytest.fixture
def gene_v4(gene_myc_hs):
    item = gene_myc_hs.copy()
    item.pop('transcriptome_annotation', None)
    item.update({
        'schema_version': '4',
        'annotation_version': 'GENCODE 42'
    })
    return item


@pytest.fixture
def gene_v5(gene_v4):
    item = gene_v4.copy()
    item.update({
        'schema_version': '5',
        'description': ''
    })
    return item


@pytest.fixture
def gene_v6(gene_myc_hs):
    item = gene_myc_hs.copy()
    item.update({
        'schema_version': '6',
        'locations': [
            {
                'assembly': 'mm9',
                'chromosome': 'chr7',
                'start': 128207872,
                'end': 128207943
            }]
    })
    return item


@pytest.fixture
def gene_v8(gene_myc_hs):
    item = gene_myc_hs.copy()
    item.update({
        'schema_version': '8',
        'synonyms': []
    })
    return item


@pytest.fixture
def gene_v9(gene_myc_hs):
    item = gene_myc_hs.copy()
    item.update(
        {
            'schema_version': '9',
            'transcriptome_annotation': 'GENCODE 28, GENCODE M17'
        }
    )
    return item
