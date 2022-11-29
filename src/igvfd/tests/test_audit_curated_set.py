import pytest


def test_audit_standards_doc(testapp, curated_set_genome, standards_document):
    testapp.patch_json(
        curated_set_genome['@id'],
        {'documents': [standards_document['@id']]}),
    res = testapp.get(curated_set_genome['@id'] + '@@index-data')
    errors = res.json['audit']
    errors_list = []
    print(res)
    for error_type in errors:
        errors_list.extend(errors[error_type])
    assert any(
        error['category'] == 'inconsistent standards document'
        for error in errors_list)
