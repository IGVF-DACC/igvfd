import pytest


def test_ntr_audit(testapp, assay_term_ntr):
    res = testapp.get(assay_term_ntr['@id'] + '@@audit')
    assert any(
        error['category'] == 'NTR term ID'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )
