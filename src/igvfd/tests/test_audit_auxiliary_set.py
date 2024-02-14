import pytest


def test_audit_auxiliary_set_with_non_sequence_files(
    testapp,
    base_auxiliary_set,
    analysis_set_with_sample,
    reference_file
):
    testapp.patch_json(
        reference_file['@id'],
        {'file_set': base_auxiliary_set['@id']}
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected file association'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        reference_file['@id'],
        {'file_set': analysis_set_with_sample['@id']}
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected file association'
        for error in res.json['audit'].get('WARNING', [])
    )
