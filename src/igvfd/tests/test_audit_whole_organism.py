import pytest


def test_audit_whole_organism_human_taxa(
        testapp, whole_organism_human, human_donor, rodent_donor):
    res = testapp.get(whole_organism_human['@id'] + '@@audit')
    assert any(
        error['category'] == 'incorrect taxa'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(whole_organism_human['@id'],
                       {'donors': [rodent_donor['@id'],
                                   human_donor['@id']]}
                       )
    res = testapp.get(whole_organism_human['@id'] + '@@audit')
    assert any(
        error['category'] == 'incorrect taxa'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_whole_organism_age(
    testapp,
    whole_organism
):
    res = testapp.get(whole_organism['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing age properties'
        for error in res.json['audit'].get('WARNING', [])
    )
