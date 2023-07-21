import pytest


def test_audit_construct_library_associated_disease(
    testapp,
    base_construct_library
):
    # If 'disease-associated variants' appears in selection_criteria, the
    # associated_diseases property must be populated
    testapp.patch_json(
        base_construct_library['@id'],
        {'selection_criteria': ['disease-associated variants']}
    )
    res = testapp.get(base_construct_library['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent variants and ontology metadata'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_construct_library_plasmid_map(
    testapp,
    base_construct_library,
    plasmid_map_document
):
    # Every ConstructLibrary should have a "plasmid map" document in
    # the documents property
    res = testapp.get(base_construct_library['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing plasmid map'
        for error in res.json['audit'].get('WARNING', [])
    )

    testapp.patch_json(
        base_construct_library['@id'],
        {'documents': [plasmid_map_document['@id']]}
    )
    res = testapp.get(base_construct_library['@id'] + '@@audit')
    assert 'missing plasmid map' not in (
        error['category'] for error in res.json['audit'].get('WARNING', [])
    )
