import pytest


def test_audit_related_multiome_datasets(
    testapp,
    construct_library_set_reporter,
    reference_file
):
    res = testapp.get(construct_library_set_reporter['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing files'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        reference_file['@id'],
        {
            'file_set': [construct_library_set_reporter['@id']]
        }
    )
    res = testapp.get(construct_library_set_reporter['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing files'
        for error in res.json['audit'].get('WARNING', [])
    )
