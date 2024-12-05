import pytest


def test_audit_missing_barcode_map(
    testapp,
    multiplexed_sample,
    tabular_file
):
    res = testapp.get(multiplexed_sample['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing barcode map'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        multiplexed_sample['@id'],
        {'barcode_map': tabular_file['@id']}
    )
    res = testapp.get(multiplexed_sample['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing barcode map'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
