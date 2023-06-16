import pytest


def test_audit_sample_sorted_fraction_parent_child_check(
    testapp,
    biosample_sorted_child,
    tissue_unsorted_parent,
    rodent_donor
):
    # A Sample that is a sorted_fraction of a parent sample should
    # share most of the parent's metadata properties
    res = testapp.get(biosample_sorted_child['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent sorted fraction metadata'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        biosample_sorted_child['@id'],
        {'donors': [rodent_donor['@id']],
         'embryonic': True}
    )
    testapp.patch_json(
        tissue_unsorted_parent['@id'],
        {'nih_institutional_certification': 'NIC000ABCD'}
    )
    res = testapp.get(biosample_sorted_child['@id'] + '@@audit')
    assert 'inconsistent sorted fraction metadata' not in (
        error['category'] for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_sample_virtual_donor_check(
    testapp, human_donor, rodent_donor, tissue
):
    # A non-virtual sample should not be linked to a virtual donor.
    testapp.patch_json(
        human_donor['@id'],
        {
            'virtual': True
        }
    ),
    testapp.patch_json(
        rodent_donor['@id'],
        {
            'virtual': True
        }
    )
    testapp.patch_json(
        tissue['@id'],
        {
            'virtual': False,
            'donors': [human_donor['@id'], rodent_donor['@id']]
        }
    )
    res = testapp.get(tissue['@id'] + '@@index-data')
    assert any(
        error['category'] == 'inconsistent sample metadata'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_virtual_sample_linked_to_non_virtual_sample_with_array_property(
    testapp,
    primary_cell_with_pooled_from
):
    # Non-virtual samples should not be linked to virtual samples
    res = testapp.get(primary_cell_with_pooled_from['@id'] + '@@index-data')
    assert any(
        error['category'] == 'virtual sample linked to non-virtual sample'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        primary_cell_with_pooled_from['@id'],
        {'virtual': False}
    )
    res = testapp.get(primary_cell_with_pooled_from['@id'] + '@@index-data')
    assert all(
        error['category'] != 'virtual sample linked to non-virtual sample'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_non_virtual_sample_linked_to_virtual_sample_with_single_property(
    testapp,
    primary_cell_with_part_of_virtual_true
):
    # Non-virtual samples should not be linked to virtual samples
    res = testapp.get(primary_cell_with_part_of_virtual_true['@id'] + '@@index-data')
    assert any(
        error['category'] == 'non-virtual sample linked to virtual sample'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        primary_cell_with_part_of_virtual_true['@id'],
        {'virtual': True}
    )
    res = testapp.get(primary_cell_with_part_of_virtual_true['@id'] + '@@index-data')
    assert all(
        error['category'] != 'non-virtual sample linked to virtual sample'
        for error in res.json['audit'].get('ERROR', [])
    )
