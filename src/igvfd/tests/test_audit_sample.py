import pytest


def test_audit_sample_sorted_from_parent_child_check(
    testapp,
    biosample_sorted_child,
    tissue_unsorted_parent,
    rodent_donor
):
    # A Sample that is a sorted_from of a parent sample should
    # share most of the parent's metadata properties
    res = testapp.get(biosample_sorted_child['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent parent sample'
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
    assert 'inconsistent parent sample' not in (
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
    tissue_res = testapp.get(tissue['@id'] + '@@index-data')
    human_donor_res = testapp.get(human_donor['@id'] + '@@index-data')
    rodent_donor_res = testapp.get(rodent_donor['@id'] + '@@index-data')
    assert any(
        error['category'] == 'inconsistent donor'
        for error in tissue_res.json['audit'].get('ERROR', [])
    )
    tissue_link = '{' + tissue_res.json['object'].get('accession') + '|' + tissue_res.json['object'].get('@id') + '}'
    human_donor_link = '{' + human_donor_res.json['object'].get(
        'accession') + '|' + human_donor_res.json['object'].get('@id') + '}'
    rodent_donor_link = '{' + rodent_donor_res.json['object'].get(
        'accession') + '|' + rodent_donor_res.json['object'].get('@id') + '}'
    assert any(
        error['detail'] == f'The sample {tissue_link} is linked to virtual donor(s): {human_donor_link}, {rodent_donor_link}'
        for error in tissue_res.json['audit'].get('ERROR', [])
    ) or any(
        error['detail'] == f'The sample {tissue_link} is linked to virtual donor(s): {rodent_donor_link}, {human_donor_link}'
        for error in tissue_res.json['audit'].get('ERROR', [])
    )


def test_virtual_sample_linked_to_non_virtual_sample_with_array_property(
    testapp,
    primary_cell_with_pooled_from
):
    # Non-virtual samples should not be linked to virtual samples
    res = testapp.get(primary_cell_with_pooled_from['@id'] + '@@index-data')
    assert any(
        error['category'] == 'inconsistent parent sample'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        primary_cell_with_pooled_from['@id'],
        {'virtual': False}
    )
    res = testapp.get(primary_cell_with_pooled_from['@id'] + '@@index-data')
    assert all(
        error['category'] != 'inconsistent parent sample'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_non_virtual_sample_linked_to_virtual_sample_with_single_property(
    testapp,
    primary_cell_with_part_of_virtual_true,
    primary_cell
):
    # Non-virtual samples should not be linked to virtual samples
    testapp.patch_json(
        primary_cell['@id'],
        {'virtual': True}
    )
    res = testapp.get(primary_cell_with_part_of_virtual_true['@id'] + '@@index-data')
    assert any(
        error['category'] == 'inconsistent parent sample'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        primary_cell_with_part_of_virtual_true['@id'],
        {'virtual': True}
    )
    res = testapp.get(primary_cell_with_part_of_virtual_true['@id'] + '@@index-data')
    assert all(
        error['category'] != 'inconsistent parent sample'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_inconsistent_construct_library_sets_types(
    testapp,
    primary_cell,
    base_expression_construct_library_set,
    construct_library_set_genome_wide,
    construct_library_set_reporter,
    construct_library_set_y2h
):
    testapp.patch_json(
        primary_cell['@id'],
        {
            'construct_library_sets': [base_expression_construct_library_set['@id'],
                                       construct_library_set_genome_wide['@id']]
        }
    )
    res = testapp.get(primary_cell['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent construct library sets'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        primary_cell['@id'],
        {
            'construct_library_sets': [base_expression_construct_library_set['@id'],
                                       construct_library_set_genome_wide['@id'],
                                       construct_library_set_reporter['@id']]
        }
    )
    res = testapp.get(primary_cell['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent construct library sets'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        primary_cell['@id'],
        {
            'construct_library_sets': [base_expression_construct_library_set['@id'], construct_library_set_y2h['@id']]
        }
    )
    res = testapp.get(primary_cell['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent construct library sets'
        for error in res.json['audit'].get('WARNING', [])
    )
