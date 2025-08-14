
def test_audit_item_schema_validation(testapp, item_donor):
    testapp.patch_json(item_donor['@id'] +
                       '?validate=false', {'disallowed': 'errs'})
    res = testapp.get(item_donor['@id'] + '@@audit')
    errors = res.json['audit']
    errors_list = []
    for error_type in errors:
        errors_list.extend(errors[error_type])
    assert any(
        error['category'] == 'validation error' and error['name'] == 'audit_item_schema'
        for error in errors_list)


def test_audit_item_schema_upgrade_failure(testapp, item_donor):
    testapp.patch_json(item_donor['@id'] +
                       '?validate=false', {'schema_version': '999'})
    res = testapp.get(item_donor['@id'] + '@@audit')
    errors = res.json['audit']
    errors_list = []
    for error_type in errors:
        errors_list.extend(errors[error_type])
    assert any(
        error['category'] == 'upgrade failure' and error['name'] == 'audit_item_schema'
        for error in errors_list)


def test_audit_item_schema_upgrade_ok(testapp, item_donor):
    patch = {
        'schema_version': '5',
        'status': 'in progress',
    }
    testapp.patch_json(item_donor['@id'] + '?validate=false', patch)
    res = testapp.get(item_donor['@id'] + '@@audit')
    errors = res.json['audit']
    errors_list = []
    for error_type in errors:
        errors_list.extend(errors[error_type])
    assert not any(error['name'] ==
                   'audit_item_schema' for error in errors_list)


def test_audit_item_schema_upgrade_validation_failure(testapp, item_donor):
    patch = {
        'schema_version': '5',
        'status': 'UNKNOWN',
    }
    testapp.patch_json(item_donor['@id'] + '?validate=false', patch)
    res = testapp.get(item_donor['@id'] + '@@audit')
    errors = res.json['audit']
    errors_list = []
    for error_type in errors:
        errors_list.extend(errors[error_type])
    assert any(
        error['category'] == 'validation error: status' and error['name'] == 'audit_item_schema'
        for error in errors_list)


def test_audit_item_mismatched_status(
    testapp,
    measurement_set,
    assay_term_starr,
    tissue
):
    testapp.patch_json(
        measurement_set['@id'],
        {'status': 'in progress'}
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'mismatched status'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )
    testapp.patch_json(
        assay_term_starr['@id'],
        {'status': 'in progress'}
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'status': 'preview',
            'preview_timestamp': '2025-03-06T12:34:56Z'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'mismatched status'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )
    testapp.patch_json(
        assay_term_starr['@id'],
        {'status': 'archived', 'release_timestamp': '2024-03-06T12:34:56Z'}
    )
    testapp.patch_json(
        measurement_set['@id'],
        {'status': 'in progress'}
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'mismatched status'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )
    testapp.patch_json(
        tissue['@id'],
        {'status': 'revoked', 'release_timestamp': '2024-03-06T12:34:56Z'}
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'mismatched status'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )
