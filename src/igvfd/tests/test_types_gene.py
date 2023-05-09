import pytest


def test_gene_homo_sapiens(gene_myc_hs, testapp):
    res = testapp.get(gene_myc_hs['@id'])
    assert res.json['title'] == 'MYC (Homo sapiens)'


def test_gene_mus_musculus(gene_zscan10_mm, testapp):
    res = testapp.get(gene_zscan10_mm['@id'])
    assert res.json['title'] == 'Zcan10 (Mus musculus)'


def test_gene_geneid_with_version(gene_zscan10_mm, testapp):
    testapp.patch_json(
        gene_zscan10_mm['@id'],
        {'version_number': '11'}
    )
    res = testapp.get(gene_zscan10_mm['@id'])
    assert res.json['geneid_with_version'] == 'ENSMUSG00000023902.11'
