import pytest


def test_audit_whole_organism_human_taxa(testapp, whole_organism_human):
    res = testapp.get(whole_organism_human['@id'] + '@@index-data')
    assert any(
        error['category'] == 'incorrect taxa'
        for error in res.json['audit'].get('ERROR', [])
    )
