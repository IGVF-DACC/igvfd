import pytest


def test_audit_whole_organism_human_taxa(
        testapp, whole_organism_human, human_donor, rodent_donor):
    res = testapp.get(whole_organism_human['@id'] + '@@index-data')
    assert any(
        error['category'] == 'incorrect taxa'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(whole_organism_human['@id'],
                       {'donors': [rodent_donor['@id'],
                                   human_donor['@id']]}
                       )
    res = testapp.get(whole_organism_human['@id'] + '@@index-data')
    assert any(
        error['category'] == 'incorrect taxa'
        for error in res.json['audit'].get('ERROR', [])
    )
