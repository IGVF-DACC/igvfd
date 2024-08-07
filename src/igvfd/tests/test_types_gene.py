import pytest


def test_gene_homo_sapiens(gene_myc_hs, testapp):
    res = testapp.get(gene_myc_hs['@id'])
    assert res.json['title'] == 'MYC (Homo sapiens)'


def test_gene_mus_musculus(gene_zscan10_mm, testapp):
    res = testapp.get(gene_zscan10_mm['@id'])
    assert res.json['title'] == 'Zcan10 (Mus musculus)'


def test_gene_geneid_with_version(gene_zscan10_mm, gene_CRLF2_par_y, testapp):
    testapp.patch_json(
        gene_zscan10_mm['@id'],
        {'version_number': '11'}
    )
    res = testapp.get(gene_zscan10_mm['@id'])
    assert res.json['geneid_with_version'] == 'ENSMUSG00000023902.11'

    res = testapp.get(gene_CRLF2_par_y['@id'])
    assert res.json['geneid_with_version'] == 'ENSG00000205755.3_PAR_Y'


def test_gene_summary(testapp, gene_myc_hs):
    res = testapp.get(gene_myc_hs['@id'])
    assert res.json.get('summary', '') == 'MYC - ENSG00000136997 (Homo sapiens)'
