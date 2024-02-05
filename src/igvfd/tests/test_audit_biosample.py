import pytest


def test_audit_biosample_taxa_check(testapp, tissue, rodent_donor, human_donor, human_male_donor):
    '''A Biosample that has donors of different taxa should not have calculated taxa property and trigger audit.'''

    testapp.patch_json(tissue['@id'],
                       {'donors': [rodent_donor['@id'],
                                   human_donor['@id'],
                                   human_male_donor['@id']]}
                       )
    res = testapp.get(tissue['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent donor taxa'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(tissue['@id'],
                       {'donors': [human_donor['@id'],
                                   human_male_donor['@id']]}
                       )
    res = testapp.get(tissue['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent donor taxa'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(tissue['@id'],
                       {'donors': [human_donor['@id']]}
                       )
    res = testapp.get(tissue['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent donor taxa'
        for error in res.json['audit'].get('ERROR', [])
    )
