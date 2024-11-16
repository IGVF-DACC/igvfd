import pytest


def test_index_file_derived_from(testapp, index_file_tbi, index_file_bai, alignment_file, controlled_access_alignment_file, tabular_file):
    # tbi must be derived_from Tabular or Reference File
    res = testapp.patch_json(
        index_file_tbi['@id'],
        {
            'derived_from': [alignment_file['@id']]
        },
        expect_errors=True
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        index_file_tbi['@id'],
        {
            'derived_from': [tabular_file['@id']]
        }
    )
    assert res.status_code == 200
    # bai must be derived_from Alignment File
    res = testapp.patch_json(
        index_file_bai['@id'],
        {
            'derived_from': [tabular_file['@id']]
        }
    )
    assert res.status_code == 422
    res = testapp.patch_json(
        index_file_tbi['@id'],
        {
            'derived_from': [alignment_file['@id']]
        }
    )
    assert res.status_code == 200
    # Cannot have array > 1 for derived_from
    res = testapp.patch_json(
        index_file_bai['@id'],
        {
            'derived_from': [
                alignment_file['@id'],
                controlled_access_alignment_file['@id']
            ]
        },
        expect_errors=True
    )
    assert res.status_code == 422
