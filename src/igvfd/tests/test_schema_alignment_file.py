import pytest


# This tests the regex that disallows submission of any pattern. Remove this test once dbxrefs are added for alignment files.
def test_restricted_dbxrefs(testapp, alignment_file):
    res = testapp.patch_json(
        alignment_file['@id'],
        {'dbxrefs': ['']}, expect_errors=True)
    assert res.status_code == 422


def test_assembly_transcriptome_dependency(testapp, alignment_file):
    res = testapp.patch_json(
        alignment_file['@id'],
        {'assembly': 'mm10',
         'transcriptome_annotation': 'GENCODE M25'})
    assert res.status_code == 200
    res = testapp.patch_json(
        alignment_file['@id'],
        {'assembly': 'mm10',
         'transcriptome_annotation': 'GENCODE M17'})
    assert res.status_code == 200
    res = testapp.patch_json(
        alignment_file['@id'],
        {'assembly': 'GRCm39',
         'transcriptome_annotation': 'GENCODE M17'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        alignment_file['@id'],
        {'assembly': 'GRCh38, mm10',
         'transcriptome_annotation': 'GENCODE 32, GENCODE M23'})
    assert res.status_code == 200
    res = testapp.patch_json(
        alignment_file['@id'],
        {'assembly': 'GRCh38',
         'transcriptome_annotation': 'GENCODE 32, GENCODE M23'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        alignment_file['@id'],
        {'assembly': 'GRCh38',
         'transcriptome_annotation': 'GENCODE 28'})
    assert res.status_code == 200
