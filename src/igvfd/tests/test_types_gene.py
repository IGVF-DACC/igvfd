import pytest


def test_gene_homo_sapiens(gene_myc_hs, testapp):
    res = testapp.get(gene_myc_hs['@id'])
    assert(res.json['title'] == 'MYC (Homo sapiens)')


def test_gene_mus_musculus(gene_zscan10_mm, testapp):
    res = testapp.get(gene_zscan10_mm['@id'])
    assert(res.json['title'] == 'Zcan10 (Mus musculus)')
