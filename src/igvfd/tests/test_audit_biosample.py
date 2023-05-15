import pytest


def test_audit_biosample_nih_institutional_certification(
    testapp,
    primary_cell
):
    res = testapp.get(primary_cell['@id'] + '@@index-data')
    assert any(
        error['category'] == 'missing nih_institutional_certification'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        primary_cell['@id'],
        {
            'nih_institutional_certification': 'NIC00042'
        }
    )
    res = testapp.get(primary_cell['@id'] + '@@index-data')
    assert all(
        error['category'] != 'missing nih_institutional_certification'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_biosample_taxa_check(testapp, tissue, rodent_donor, human_donor, human_male_donor):
    '''A Biosample that has donors of different taxa should not have calculated taxa property and trigger audit.'''

    testapp.patch_json(tissue['@id'],
                       {'donors': [rodent_donor['@id'],
                                   human_donor['@id']]}
                       )
    res = testapp.get(tissue['@id'] + '@@index-data')
    assert any(
        error['category'] == 'inconsistent donor taxa'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(tissue['@id'],
                       {'donors': [human_donor['@id'],
                                   human_male_donor['@id']]}
                       )
    res = testapp.get(tissue['@id'] + '@@index-data')
    assert all(
        error['category'] != 'inconsistent donor taxa'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(tissue['@id'],
                       {'donors': [human_donor['@id']]}
                       )
    res = testapp.get(tissue['@id'] + '@@index-data')
    assert all(
        error['category'] != 'inconsistent donor taxa'
        for error in res.json['audit'].get('ERROR', [])
    )
