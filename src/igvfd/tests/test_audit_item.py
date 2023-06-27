
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
