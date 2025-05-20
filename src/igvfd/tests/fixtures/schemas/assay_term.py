import pytest


@pytest.fixture
def assay_term_starr(testapp):
    item = {
        'term_id': 'OBI:0002041',
        'term_name': 'STARR-seq'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_chip(testapp):
    item = {
        'term_id': 'OBI:0002017',
        'term_name': 'ChIP-seq assay'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_dnase(testapp):
    item = {
        'term_id': 'OBI:0001853',
        'term_name': 'DNase-seq'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_atac(testapp):
    item = {
        'term_id': 'OBI:002039',
        'term_name': 'ATAC-seq'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_rna(testapp):
    item = {
        'term_id': 'OBI:0001271',
        'term_name': 'RNA-seq'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_bulk_rna(testapp):
    item = {
        'term_id': 'OBI:0003090',
        'term_name': 'bulk RNA-seq assay'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_scrna(testapp):
    item = {
        'term_id': 'OBI:0002631',
        'term_name': 'single-cell RNA sequencing assay'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_scatac(testapp):
    item = {
        'term_id': 'OBI:0002762',
        'term_name': 'single-nucleus ATAC-seq'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_ntr(testapp):
    item = {
        'term_id': 'NTR:00001',
        'term_name': 'example-tn-1'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_mpra(testapp):
    item = {
        'term_id': 'OBI:0002675',
        'term_name': 'massively parallel reporter assay'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_crispr(testapp):
    item = {
        'term_id': 'OBI:0003659',
        'term_name': 'in vitro CRISPR screen assay'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_crispr_single_cell(testapp):
    item = {
        'term_id': 'OBI:0003660',
        'term_name': 'in vitro CRISPR screen using single-cell RNA-seq'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_cas_mediated_mutagenesis(testapp):
    item = {
        'term_id': 'OBI:0003133',
        'term_name': 'cas mediated mutagenesis'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_y2h(testapp):
    item = {
        'term_id': 'OBI:0000288',
        'term_name': 'protein-protein interaction detection assay'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_CRISPR_sorted(testapp):
    item = {
        'term_id': 'OBI:0003661',
        'term_name': 'in vitro CRISPR screen using flow cytometry'
    }
    return testapp.post_json('/assay_term', item, status=201).json['@graph'][0]


@pytest.fixture
def assay_term_v1(assay_term_starr):
    item = assay_term_starr.copy()
    item.update({
        'schema_version': '1',
        'aliases': []
    })
    return item


@pytest.fixture
def assay_term_v2(assay_term_v1):
    item = assay_term_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item


@pytest.fixture
def assay_term_v3(assay_term_crispr):
    item = assay_term_crispr.copy()
    item.update({
        'schema_version': '3',
        'preferred_assay_titles': ['histone ChIP-seq', 'Parse Split-seq', 'Saturation genome editing', 'SHARE-Seq', 'Yeast two-hybrid', 'Cell painting']
    })
    return item


@pytest.fixture
def assay_term_v5(assay_term_crispr):
    item = assay_term_crispr.copy()
    item.update({
        'schema_version': '5',
        'preferred_assay_titles': []
    })
    return item


@pytest.fixture
def assay_term_v6(assay_term_crispr):
    item = assay_term_crispr.copy()
    item.update({
        'schema_version': '6',
        'preferred_assay_titles': ['Variant FlowFISH', 'CRISPR FlowFISH']
    })
    return item


@pytest.fixture
def assay_term_v7(assay_term_crispr):
    item = assay_term_crispr.copy()
    item.update({
        'schema_version': '7',
        'preferred_assay_titles': ['Variant painting']
    })
    return item


@pytest.fixture
def assay_term_v8(assay_term_crispr):
    item = assay_term_crispr.copy()
    item.update({
        'schema_version': '8',
        'preferred_assay_titles': ['Variant FlowFISH']
    })
    return item


@pytest.fixture
def assay_term_v9(assay_term_crispr):
    item = assay_term_crispr.copy()
    item.update({
        'schema_version': '9',
        'preferred_assay_titles': ['scMito-seq']
    })
    return item


@pytest.fixture
def assay_term_v10(assay_term_crispr):
    item = assay_term_crispr.copy()
    item.update({
        'schema_version': '10',
        'preferred_assay_titles': ['Growth CRISPR screen']
    })
    return item


@pytest.fixture
def assay_term_v11(assay_term_crispr):
    item = assay_term_crispr.copy()
    item.update({
        'schema_version': '11',
        'definition': 'test definition',
        'comment': 'test comment'
    })
    return item


@pytest.fixture
def assay_term_v12(assay_term_crispr):
    item = assay_term_crispr.copy()
    item.update({
        'schema_version': '12',
        'preferred_assay_titles': ['SUPERSTARR']
    })
    return item
