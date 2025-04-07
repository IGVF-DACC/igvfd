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
        {'ccf_id': '78d06f07-f1cb-4d21-b578-b01c7388804f'}
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
    assert any(
        error['category'] == 'inconsistent donor'
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


def test_audit_parent_sample_singular_children(
    testapp,
    in_vitro_cell_line,
    in_vitro_differentiated_cell,
    in_vitro_organoid
):
    testapp.patch_json(
        in_vitro_differentiated_cell['@id'],
        {
            'originated_from': in_vitro_cell_line['@id']
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing sample'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )
    testapp.patch_json(
        in_vitro_organoid['@id'],
        {
            'originated_from': in_vitro_cell_line['@id']
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing sample'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )


def test_audit_missing_nucleic_acid_delivery(
    testapp,
    in_vitro_cell_line,
    construct_library_set_genome_wide
):
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'construct_library_sets': [construct_library_set_genome_wide['@id']]
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing nucleic acid delivery'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'nucleic_acid_delivery': 'lipofectamine'
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing nucleic acid delivery'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_missing_publication(
    testapp,
    in_vitro_cell_line,
    publication
):
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert res.json.get('publications', '') == ''
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'status': 'released',
            'release_timestamp': '2025-03-06T12:34:56Z'
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing publication'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'publications': [publication['@id']]
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing publication'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )


def test_audit_missing_association(
    testapp,
    pooled_from_primary_cell,
    in_vitro_cell_line
):
    res = testapp.get(pooled_from_primary_cell['@id']).json
    assert (all(not res.get(prop) for prop in ['file_sets', 'origin_of',
            'parts', 'sorted_fractions', 'multiplexed_in', 'pooled_in']))
    res = testapp.get(pooled_from_primary_cell['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing association'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'part_of': pooled_from_primary_cell['@id']
        }
    )
    res = testapp.get(pooled_from_primary_cell['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing association'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )
