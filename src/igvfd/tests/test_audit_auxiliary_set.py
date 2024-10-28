import pytest


def test_audit_auxiliary_set_with_non_sequence_files(
    testapp,
    base_auxiliary_set,
    principal_analysis_set,
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
        {'file_set': principal_analysis_set['@id']}
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


def test_audit_missing_measurement_sets(
    testapp,
    auxiliary_set_cell_sorting,
    measurement_set
):
    res = testapp.get(auxiliary_set_cell_sorting['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing measurement set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'auxiliary_sets': [auxiliary_set_cell_sorting['@id']]
        }
    )
    res = testapp.get(auxiliary_set_cell_sorting['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing measurement set'
        for error in res.json['audit'].get('ERROR', [])
    )
