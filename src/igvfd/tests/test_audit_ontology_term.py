import pytest


def test_ntr_audit(testapp, assay_term_ntr):
    res = testapp.get(assay_term_ntr['@id'] + '@@audit')
    assert any(
        error['category'] == 'NTR term ID'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )


def test_audit_missing_ontology_reference(testapp, assay_term_starr):
    patch_res = testapp.patch_json(
        assay_term_starr['@id'],
        {'term_id': 'OBI:99999999'},
        status=200,
    )
    # Changing term_id updates the accession path; use the returned @id.
    updated_id = patch_res.json['@graph'][0]['@id']
    res = testapp.get(updated_id + '@@audit')
    assert any(
        error['category'] == 'missing ontology reference'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )


def test_audit_inconsistent_ontology_term(testapp, assay_term_starr):
    testapp.patch_json(
        assay_term_starr['@id'],
        {'term_name': 'ontology term name does not match reference'},
        status=200,
    )
    res = testapp.get(assay_term_starr['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent ontology term'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_inconsistent_ontology_term_not_triggered_for_canonical_name(
    testapp, assay_term_starr
):
    testapp.patch_json(
        assay_term_starr['@id'],
        {
            'term_name': (
                'self-transcribing active regulatory region sequencing assay'
            )
        },
        status=200,
    )
    res = testapp.get(assay_term_starr['@id'] + '@@audit')
    errors = res.json['audit'].get('ERROR', [])
    assert not any(
        error['category'] == 'inconsistent ontology term' for error in errors
    )


def test_audit_ntr_skips_inconsistent_ontology_term(testapp, assay_term_ntr):
    res = testapp.get(assay_term_ntr['@id'] + '@@audit')
    errors = res.json['audit'].get('ERROR', [])
    assert not any(
        error['category'] == 'inconsistent ontology term' for error in errors
    )
