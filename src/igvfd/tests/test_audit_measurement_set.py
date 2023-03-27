import pytest


def test_audit_related_multiome_datasets(
    testapp,
    primary_cell,
    in_vitro_cell_line,
    tissue,
    measurement_set_multiome,
    measurement_set_multiome_2,
    measurement_set
):
    # If `multiome_size` is specified, `related_multiome_datasets` should not be empty.
    res = testapp.get(measurement_set_multiome['@id'] + '@@index-data')
    assert any(
        error['category'] == 'inconsistent multiome metadata'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
    res = testapp.get(measurement_set_multiome['@id'] + '@@index-data')
    assert any(
        error['category'] == 'inconsistent multiome metadata'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        measurement_set_multiome_2['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
    res = testapp.get(measurement_set_multiome['@id'] + '@@index-data')
    assert res.json['audit'].get('WARNING', []) == []
    # the length of `related_multiome_datasets` array and `multiome_size` - 1 should be the same
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'multiome_size': 4
        }
    )
    testapp.patch_json(
        measurement_set_multiome_2['@id'],
        {
            'multiome_size': 4
        }
    )
    res = testapp.get(measurement_set_multiome['@id'] + '@@index-data')
    assert any(
        error['category'] == 'inconsistent multiome metadata'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'multiome_size': 2
        }
    )
    testapp.patch_json(
        measurement_set_multiome_2['@id'],
        {
            'multiome_size': 2
        }
    )
    res = testapp.get(measurement_set_multiome['@id'] + '@@index-data')
    assert res.json['audit'].get('WARNING', []) == []
    # `samples` should be the same between other datasets in `related_multiome_datasets`
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'samples': [primary_cell['@id'], in_vitro_cell_line['@id']]
        }
    )
    res = testapp.get(measurement_set_multiome['@id'] + '@@index-data')
    assert any(
        error['category'] == 'inconsistent multiome metadata'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        measurement_set_multiome_2['@id'],
        {
            'samples': [primary_cell['@id'], in_vitro_cell_line['@id']]
        }
    )
    res = testapp.get(measurement_set_multiome['@id'] + '@@index-data')
    assert res.json['audit'].get('WARNING', []) == []
    # `multiome_size` should be the same between other datasets in `related_multiome_datasets`
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'multiome_size': 3
        }
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [primary_cell['@id'], in_vitro_cell_line['@id']]
        }
    )
    res = testapp.get(measurement_set_multiome['@id'] + '@@index-data')
    assert any(
        error['category'] == 'inconsistent multiome metadata'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        measurement_set_multiome_2['@id'],
        {
            'multiome_size': 3
        }
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'multiome_size': 3
        }
    )
    res = testapp.get(measurement_set_multiome['@id'] + '@@index-data')
    assert res.json['audit'].get('WARNING', []) == []
