import pytest


def test_transcriptome_annotation_dependency(testapp, reference_file):
    res = testapp.patch_json(
        reference_file['@id'],
        {
            'assembly': 'GRCh38',
            'transcriptome_annotation': 'GENCODE M32'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        reference_file['@id'],
        {
            'assembly': 'GRCh38',
            'transcriptome_annotation': 'GENCODE 40'
        }
    )
    assert res.status_code == 200
    res = testapp.patch_json(
        reference_file['@id'],
        {
            'assembly': 'GRCm39',
            'transcriptome_annotation': 'GENCODE M30'
        }
    )
    assert res.status_code == 200
    res = testapp.patch_json(
        reference_file['@id'],
        {
            'assembly': 'GRCm39',
            'transcriptome_annotation': 'GENCODE 40'
        }, expect_errors=True
    )
    assert res.status_code == 422
