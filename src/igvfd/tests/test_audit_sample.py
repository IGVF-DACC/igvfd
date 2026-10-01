def test_audit_sample_sorted_from_parent_child_check(
    testapp,
    biosample_sorted_child,
    tissue_unsorted_parent,
    rodent_donor,
    lab,
    award,
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
        {'product_id': 'ABC999'}
    )
    res = testapp.get(biosample_sorted_child['@id'] + '@@audit')
    assert 'inconsistent parent sample' not in (
        error['category'] for error in res.json['audit'].get('ERROR', [])
    )
    # If parent sample doesn't have anvil status and the child does (no audit)
    testapp.patch_json(
        biosample_sorted_child['@id'],
        {'is_on_anvil': True}
    )
    res = testapp.get(biosample_sorted_child['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent parent sample'
        for error in res.json['audit'].get('ERROR', [])
    )
    # If checking unsorted array properties such as construct delivery methods
    testapp.patch_json(
        biosample_sorted_child['@id'],
        {'construct_delivery_methods': ['lipofectamine', 'electroporation']}
    )
    testapp.patch_json(
        tissue_unsorted_parent['@id'],
        {'construct_delivery_methods': ['electroporation', 'lipofectamine']}
    )
    res = testapp.get(biosample_sorted_child['@id'] + '@@audit')
    assert 'inconsistent parent sample' not in (
        error['category'] for error in res.json['audit'].get('ERROR', [])
    )
    # Biomarkers may differ between sorted_from child and parent without audit
    biomarker = testapp.post_json(
        '/biomarker',
        {
            'name': 'CDH5',
            'quantification': 'high',
            'classification': 'marker gene',
            'award': award['@id'],
            'lab': lab['@id'],
        }
    ).json['@graph'][0]
    testapp.patch_json(
        biosample_sorted_child['@id'],
        {'biomarkers': [biomarker['@id']]}
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


def test_audit_missing_construct_delivery_methods(
    testapp,
    in_vitro_cell_line,
    multiplexed_sample,
    construct_library_set_genome_wide
):
    # Audit: In vitro cell line with construct_library_sets but missing construct_delivery_methods
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'construct_library_sets': [construct_library_set_genome_wide['@id']]
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing construct delivery methods'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    # No audit for in vitro cell line with construct_delivery_methods added
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'construct_delivery_methods': ['lipofectamine']
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing construct delivery methods'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    # No audit for multiplexed sample with construct_library_sets but missing construct_delivery_methods
    res = testapp.get(multiplexed_sample['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing construct delivery methods'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
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


def test_audit_missing_moi_warning(
    testapp,
    tissue,
    technical_sample,
    construct_library_set_genome_wide
):
    for sample in [tissue, technical_sample]:
        # No audit without lentiviral transduction.
        res = testapp.get(sample['@id'] + '@@audit')
        assert all(
            error['category'] != 'missing moi'
            for error in res.json['audit'].get('WARNING', [])
        )
        testapp.patch_json(
            sample['@id'],
            {'construct_delivery_methods': ['electroporation']}
        )
        res = testapp.get(sample['@id'] + '@@audit')
        assert all(
            error['category'] != 'missing moi'
            for error in res.json['audit'].get('WARNING', [])
        )
        # Lentiviral transduction without MOI triggers a warning.
        testapp.patch_json(
            sample['@id'],
            {'construct_delivery_methods': ['electroporation', 'lentiviral transduction']}
        )
        res = testapp.get(sample['@id'] + '@@audit')
        assert any(
            error['category'] == 'missing moi'
            for error in res.json['audit'].get('WARNING', [])
        )
        assert all(
            error['category'] != 'missing moi'
            for error in res.json['audit'].get('NOT_COMPLIANT', [])
        )
        # Reporting MOI clears the warning, including when MOI is zero.
        for moi in [0, 1.5]:
            testapp.patch_json(
                sample['@id'],
                {
                    'construct_library_sets': [construct_library_set_genome_wide['@id']],
                    'moi': moi
                }
            )
            res = testapp.get(sample['@id'] + '@@audit')
            assert all(
                error['category'] != 'missing moi'
                for error in res.json['audit'].get('WARNING', [])
            )


def test_audit_missing_moi_perturb_seq(
    testapp,
    tissue,
    technical_sample,
    measurement_set,
    measurement_set_perturb_seq,
    construct_library_set_genome_wide
):
    # A sample linked to both Perturb-seq and another assay gets NOT_COMPLIANT.
    testapp.patch_json(
        tissue['@id'],
        {'construct_delivery_methods': ['lentiviral transduction']}
    )
    res = testapp.get(tissue['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing moi'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    assert all(
        error['category'] != 'missing moi'
        for error in res.json['audit'].get('WARNING', [])
    )
    # Removing the Perturb-seq association leaves a warning for the other assay.
    testapp.patch_json(
        measurement_set_perturb_seq['@id'],
        {'samples': [technical_sample['@id']]}
    )
    res = testapp.get(tissue['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing moi'
        for error in res.json['audit'].get('WARNING', [])
    )
    assert all(
        error['category'] != 'missing moi'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        measurement_set_perturb_seq['@id'],
        {'samples': [tissue['@id']]}
    )
    # Reporting MOI clears the audit for Perturb-seq, including zero.
    for moi in [0, 1.5]:
        testapp.patch_json(
            tissue['@id'],
            {
                'construct_library_sets': [construct_library_set_genome_wide['@id']],
                'moi': moi
            }
        )
        res = testapp.get(tissue['@id'] + '@@audit')
        assert all(
            error['category'] != 'missing moi'
            for error in res.json['audit'].get('NOT_COMPLIANT', [])
        )
        assert all(
            error['category'] != 'missing moi'
            for error in res.json['audit'].get('WARNING', [])
        )
