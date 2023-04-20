import pytest


def test_audit_related_donors(
    testapp,
    human_donor,
    parent_human_donor_1,
    parent_human_donor_2,
    parent_human_donor_3
):
    # Related donors should not have duplicated donor objects and should mutually specify one another
    testapp.patch_json(
        human_donor['@id'],
        {
            'related_donors': [{'donor': parent_human_donor_1['@id'], 'relationship_type': 'parent'},
                               {'donor': parent_human_donor_2['@id'], 'relationship_type': 'parent'},
                               {'donor': parent_human_donor_1['@id'], 'relationship_type': 'second cousin'}]
        }
    )
    res = testapp.get(human_donor['@id'] + '@@index-data')
    assert any(
        error['category'] == 'inconsistent related donors metadata'
        for error in res.json['audit'].get('WARNING', [])
    )
    assert any(
        error['category'] == 'inconsistent related donors metadata'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        human_donor['@id'],
        {
            'related_donors': [{'donor': parent_human_donor_1['@id'], 'relationship_type': 'parent'}]
        }
    )
    testapp.patch_json(
        parent_human_donor_1['@id'],
        {
            'related_donors': [{'donor': human_donor['@id'], 'relationship_type': 'child'}]
        }
    )
    res = testapp.get(human_donor['@id'] + '@@index-data')
    assert all(
        error['category'] != 'inconsistent related donors metadata'
        for error in res.json['audit'].get('WARNING', [])
    )
    assert all(
        error['category'] != 'inconsistent related donors metadata'
        for error in res.json['audit'].get('ERROR', [])
    )
    # A donor should inherit audits from a related donor
    testapp.patch_json(
        parent_human_donor_1['@id'],
        {
            'related_donors': [{'donor': parent_human_donor_2['@id'], 'relationship_type': 'child'},
                               {'donor': parent_human_donor_2['@id'], 'relationship_type': 'second cousin'}]
        }
    )
    res = testapp.get(human_donor['@id'] + '@@index-data')
    assert any(
        error['category'] == 'inconsistent related donors metadata'
        for error in res.json['audit'].get('WARNING', [])
    )
    assert any(
        error['category'] == 'inconsistent related donors metadata'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        parent_human_donor_1['@id'],
        {
            'related_donors': [{'donor': human_donor['@id'], 'relationship_type': 'child'},
                               {'donor': parent_human_donor_2['@id'], 'relationship_type': 'second cousin'}]
        }
    )
    testapp.patch_json(
        parent_human_donor_2['@id'],
        {
            'related_donors': [{'donor': human_donor['@id'], 'relationship_type': 'child'},
                               {'donor': parent_human_donor_1['@id'], 'relationship_type': 'second cousin'}]
        }
    )
    res = testapp.get(human_donor['@id'] + '@@index-data')
    assert all(
        error['category'] != 'inconsistent related donors metadata'
        for error in res.json['audit'].get('WARNING', [])
    )
    assert all(
        error['category'] != 'inconsistent related donors metadata'
        for error in res.json['audit'].get('ERROR', [])
    )
