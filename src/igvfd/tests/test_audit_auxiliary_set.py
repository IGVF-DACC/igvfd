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
        error['category'] == 'unexpected files'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        reference_file['@id'],
        {'file_set': analysis_set_with_sample['@id']}
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected files'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_unexpected_virtual_sample(
    testapp,
    base_auxiliary_set,
    in_vitro_cell_line
):
    testapp.patch_json(
        base_auxiliary_set['@id'],
        {
            'samples': [in_vitro_cell_line['@id']]
        }
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected sample'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'virtual': True
        }
    )
    res = testapp.get(base_auxiliary_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected sample'
        for error in res.json['audit'].get('ERROR', [])
    )
