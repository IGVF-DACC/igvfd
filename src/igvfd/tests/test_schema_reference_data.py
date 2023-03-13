import pytest


def test_transcriptome_annotation_dependency(testapp, reference_data):
    res = testapp.patch_json(
        reference_data['@id'],
        {
            'assembly': 'GRCh38',
            'transcriptome_annotation': 'M32'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        reference_data['@id'],
        {
            'assembly': 'GRCh38',
            'transcriptome_annotation': 'V40'
        }
    )
    assert res.status_code == 200
    res = testapp.patch_json(
        reference_data['@id'],
        {
            'assembly': 'GRCm39',
            'transcriptome_annotation': 'M30'
        }
    )
    assert res.status_code == 200
    res = testapp.patch_json(
        reference_data['@id'],
        {
            'assembly': 'GRCm39',
            'transcriptome_annotation': 'V40'
        }, expect_errors=True
    )
    assert res.status_code == 422
