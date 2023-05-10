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
        error['category'] == 'missing associated_diseases ontology or disease-associated variants'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )

    # If 'disease-associated variants' appears in origins, the
    # associated_diseases property must be populated
    edited_lib = testapp.get(base_construct_library['@id'] + '@@edit').json
    edited_lib.pop('associated_diseases')
    testapp.put_json(base_construct_library['@id'], edited_lib)
    res = testapp.get(base_construct_library['@id'] + '@@index-data')
    assert 'missing associated_diseases ontology or disease-associated variants' not in (
        error['category'] for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        base_construct_library['@id'],
        {'origins': ['disease-associated variants']}
    )
    res = testapp.get(base_construct_library['@id'] + '@@index-data')
    assert any(
        error['category'] == 'missing associated_diseases ontology or disease-associated variants'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_construct_library_plasmid_map(
    testapp,
    base_construct_library,
    plasmid_map_document
):
    # Every ConstructLibrary should have a "plasmid map" document in
    # the documents property
    res = testapp.get(base_construct_library['@id'] + '@@index-data')
    assert any(
        error['category'] == 'missing plasmid map'
        for error in res.json['audit'].get('WARNING', [])
    )

    testapp.patch_json(
        base_construct_library['@id'],
        {'documents': [plasmid_map_document['@id']]}
    )
    res = testapp.get(base_construct_library['@id'] + '@@index-data')
    assert 'missing plasmid map' not in (
        error['category'] for error in res.json['audit'].get('WARNING', [])
    )
