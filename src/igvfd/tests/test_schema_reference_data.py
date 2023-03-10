import pytest


def test_transcriptome_annotation_dependency(testapp, reference_data):
    res = testapp.patch_json(
        reference_data['@id'],
        {
            'transcriptome_annotation': 'M30'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        reference_data['@id'],
        {
            'transcriptome_annotation': 'M31'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        reference_data['@id'],
        {
            'transcriptome_annotation': 'M32'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        reference_data['@id'],
        {
            'transcriptome_annotation': 'V40'
        }
    )
    assert res.status_code == 200
    res = testapp.patch_json(
        reference_data['@id'],
        {
            'transcriptome_annotation': 'V41'

        }
    )
    assert res.status_code == 200
    res = testapp.patch_json(
        reference_data['@id'],
        {
            'transcriptome_annotation': 'V42'

        }
    )
    assert res.status_code == 200
    res = testapp.patch_json(
        reference_data['@id'],
        {
            'transcriptome_annotation': 'V43'

        }
    )
    assert res.status_code == 200
