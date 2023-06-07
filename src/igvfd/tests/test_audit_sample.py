import pytest


def test_audit_sample_sorted_fraction_parent_child_check(
    testapp,
    biosample_sorted_child,
    tissue_unsorted_parent,
    rodent_donor
):
    # A Sample that is a sorted_fraction of a parent sample should
    # share most of the parent's metadata properties
    res = testapp.get(biosample_sorted_child['@id'] + '@@index-data')
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
    res = testapp.get(biosample_sorted_child['@id'] + '@@index-data')
    assert 'inconsistent sorted fraction metadata' not in (
        error['category'] for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_sample_virtual_donor_check(
    testapp,
    virtual_tissue_with_virtual_donor,
    nonvirtual_tissue_with_virtual_donor
):
    # A non-virtual sample should not be linked to a virtual donor.
    # Testing both virtual sample with virtual donor and non-virtual sample with virtual donor.
    res = testapp.get(virtual_tissue_with_virtual_donor['@id'] + '@@index-data')
    print('RES1: ', res)
    assert 'non-virtual sample linked to virtual donor' not in (
        error['category'] for error in res.json['audit'].get('ERROR', [])
    )

    res = testapp.get(nonvirtual_tissue_with_virtual_donor['@id'] + '@@index-data')
    print('RES2: ', res)
    assert any(
        error['category'] == 'non-virtual sample linked to virtual donor'
        for error in res.json['audit'].get('ERROR', [])
    )
