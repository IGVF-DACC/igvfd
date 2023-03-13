import pytest


def test_audit_construct_library_associated_disease(
    testapp,
    base_construct_library,
    phenotype_term_alzheimers
):
    # If associated_diseases property is used, 'disease-associated variants'
    # should appear in origins property
    testapp.patch_json(
        base_construct_library['@id'],
        {'associated_diseases': [phenotype_term_alzheimers['@id']]}
    )
    res = testapp.get(base_construct_library['@id'] + '@@index-data')
    assert any(
        error['category'] == 'missing metadata'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )

    # If 'disease-associated variants' appears in origins, the
    # associated_diseases property must be populated
    edited_lib = testapp.get(base_construct_library['@id'] + '@@edit').json
    edited_lib.pop('associated_diseases')
    testapp.put_json(base_construct_library['@id'], edited_lib)
    res = testapp.get(base_construct_library['@id'] + '@@index-data')
    assert 'missing metadata' not in (
        error['category'] for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        base_construct_library['@id'],
        {'origins': ['disease-associated variants']}
    )
    res = testapp.get(base_construct_library['@id'] + '@@index-data')
    assert any(
        error['category'] == 'missing metadata'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
