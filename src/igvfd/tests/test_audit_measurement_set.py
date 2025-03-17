import pytest


def test_audit_missing_multiome_size(
    testapp,
    measurement_set
):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'preferred_assay_title': '10x multiome'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing multiome size'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'preferred_assay_title': '10x multiome with scMito-seq'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing multiome size'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'preferred_assay_title': '10x multiome with MULTI-seq'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing multiome size'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'multiome_size': 2
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing multiome size'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'preferred_assay_title': 'Perturb-seq'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected multiome size'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_related_multiome_datasets(
    testapp,
    primary_cell,
    measurement_set_multiome,
    measurement_set_multiome_2,
    measurement_set
):
    # If `multiome_size` is specified, `related_multiome_datasets` should not be empty.
    res = testapp.get(measurement_set_multiome['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent multiome datasets'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
    res = testapp.get(measurement_set_multiome['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent multiome datasets'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        measurement_set_multiome_2['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
    res = testapp.get(measurement_set_multiome['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent multiome datasets'
        for error in res.json['audit'].get('ERROR', [])
    )
    # the length of `related_multiome_datasets` array and `multiome_size` - 1 should be the same
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'multiome_size': 4
        }
    )
    testapp.patch_json(
        measurement_set_multiome_2['@id'],
        {
            'multiome_size': 4
        }
    )
    res = testapp.get(measurement_set_multiome['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent multiome datasets'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'multiome_size': 2
        }
    )
    testapp.patch_json(
        measurement_set_multiome_2['@id'],
        {
            'multiome_size': 2
        }
    )
    res = testapp.get(measurement_set_multiome['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent multiome datasets'
        for error in res.json['audit'].get('ERROR', [])
    )
    # `multiome_size` should be the same between other datasets in `related_multiome_datasets`
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'multiome_size': 3
        }
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
    res = testapp.get(measurement_set_multiome['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent multiome datasets'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        measurement_set_multiome_2['@id'],
        {
            'multiome_size': 3
        }
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'multiome_size': 3
        }
    )
    res = testapp.get(measurement_set_multiome['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent multiome datasets'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_protocol(
    testapp,
    measurement_set
):
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing protocol'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'protocols': ['https://www.protocols.io/view/example_protocol']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing protocol'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_missing_modification(
    testapp,
    measurement_set,
    assay_term_crispr,
    tissue,
    crispr_modification_activation
):
    # CRISPR screens must also have modifications on all their samples
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_crispr['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing modification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        tissue['@id'],
        {
            'modifications': [crispr_modification_activation['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing modification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_inherit_nested_audits(
    testapp,
    measurement_set,
    primary_cell,
    treatment_chemical
):
    testapp.patch_json(
        treatment_chemical['@id'],
        {
            'treatment_term_id': 'NTR:0001185'
        }
    )
    testapp.patch_json(
        primary_cell['@id'],
        {
            'treatments': [treatment_chemical['@id']]
        }
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'NTR term ID'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )


def test_audit_preferred_assay_title(
    testapp,
    measurement_set,
    assay_term_starr
):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_starr['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent preferred assay title'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        assay_term_starr['@id'],
        {
            'preferred_assay_titles': ['SUPERSTARR']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent preferred assay title'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_missing_institutional_certification(
    testapp,
    measurement_set,
    assay_term_mpra,
    lab,
    other_lab,
    tissue,
    multiplexed_sample,
    human_donor,
    assay_term_chip,
    institutional_certificate,
    controlled_sequence_file_object,
    analysis_set_base
):
    # No audit when there are no associated human donors.
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing NIH certification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )

    # Characterization assays are skipped
    testapp.patch_json(
        tissue['@id'],
        {
            'donors': [human_donor['@id']]
        }
    )
    # Characterization assays are skipped
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_mpra['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing NIH certification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )

    # Characterization assays with controlled_access files are audited
    testapp.patch_json(
        controlled_sequence_file_object['@id'],
        {
            'file_set': measurement_set['@id'],
            'controlled_access': True
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing NIH certification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        controlled_sequence_file_object['@id'],
        {
            'file_set': analysis_set_base['@id']
        }
    )

    # Non-characterization assays are audited
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_chip['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing NIH certification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )

    # If the Measurement Set studies a Multiplexed Sample,
    # its input samples are checked for their NIC.
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [multiplexed_sample['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing NIH certification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    assert any(
        f'multiplexed in [{multiplexed_sample["accession"]}]' in error['detail']
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )

    # No flag if the NIC's lab and award match the Measurement Set.
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [tissue['@id']]
        }
    )
    testapp.patch_json(
        institutional_certificate['@id'],
        {
            'samples': [tissue['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing NIH certification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )

    # Flag when lab or award doesn't match the Measurement Set.
    testapp.patch_json(
        institutional_certificate['@id'],
        {
            'lab': other_lab['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing NIH certification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )

    # If the file set's lab is a partner lab on the IC, don't flag.
    testapp.patch_json(
        institutional_certificate['@id'],
        {
            'partner_labs': [lab['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing NIH certification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_missing_seqspec(
    testapp,
    measurement_set,
    sequence_file,
    configuration_file_seqspec,
    assay_term_scrna
):
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': measurement_set['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing sequence specification'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_scrna['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing sequence specification'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )
    assert any(
        error['category'] == 'missing sequence specification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing sequence specification'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )


def test_audit_files_associated_with_incorrect_fileset(
    testapp,
    measurement_set,
    measurement_set_multiome,
    sequence_file,
    configuration_file_seqspec,
):
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'file_set': measurement_set['@id'],
            'seqspec_of': [sequence_file['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing related files'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': measurement_set['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing related files'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': measurement_set_multiome['@id']
        }
    )
    res = testapp.get(measurement_set_multiome['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing related files'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'file_set': measurement_set_multiome['@id']
        }
    )
    res = testapp.get(measurement_set_multiome['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing related files'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_inconsistent_seqspec(
    testapp,
    measurement_set,
    sequence_file,
    sequence_file_sequencing_run_2,
    configuration_file_seqspec,
    configuration_file_seqspec_2,
    assay_term_scrna
):
    # sequence files from the same sequencing run should link to the same seqspec
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': measurement_set['@id'],
            'illumina_read_type': 'R1',
            'sequencing_run': 1,
            'flowcell_id': 'HJTW3BBXY',
            'lane': 1,
            'index': 'ACTG'
        }
    )
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'file_set': measurement_set['@id'],
            'illumina_read_type': 'R2',
            'sequencing_run': 1,
            'flowcell_id': 'HJTW3BBXY',
            'lane': 1,
            'index': 'ACTG'
        }
    )
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file['@id']]
        }
    )
    testapp.patch_json(
        configuration_file_seqspec_2['@id'],
        {
            'seqspec_of': [sequence_file_sequencing_run_2['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent sequence specifications'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file['@id'], sequence_file_sequencing_run_2['@id']]
        }
    )
    testapp.patch_json(
        configuration_file_seqspec_2['@id'],
        {
            'seqspec_of': [sequence_file['@id'], sequence_file_sequencing_run_2['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent sequence specifications'
        for error in res.json['audit'].get('ERROR', [])
    )
    # sequence files from single cell assays with different sequencing runs should not link to the same seqspec
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'sequencing_run': 2
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent sequence specifications'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_scrna['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent sequence specifications'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        configuration_file_seqspec_2['@id'],
        {
            'seqspec_of': [sequence_file_sequencing_run_2['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent sequence specifications'
        for error in res.json['audit'].get('ERROR', [])
    )
    # sequence files from the same index should link to the same seqspec
    testapp.patch_json(
        sequence_file['@id'],
        {
            'index': 'GATT'
        }
    )
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'index': 'GATT',
            'sequencing_run': 1
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent sequence specifications'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        configuration_file_seqspec['@id'],
        {
            'seqspec_of': [sequence_file['@id'], sequence_file_sequencing_run_2['@id']],
        }
    )
    testapp.patch_json(
        configuration_file_seqspec_2['@id'],
        {
            'seqspec_of': [sequence_file['@id'], sequence_file_sequencing_run_2['@id']],
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent sequence specifications'
        for error in res.json['audit'].get('ERROR', [])
    )
    # sequence files from different indices should not link to the same seqspec
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'index': 'TACA'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent sequence specifications'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_inconsistent_sequencing_kit(
    testapp,
    measurement_set,
    sequence_file,
    sequence_file_sequencing_run_2,
    platform_term_NovaSeq,
    assay_term_scrna
):
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': measurement_set['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing sequencing kit'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_scrna['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing sequencing kit'
        for error in res.json['audit'].get('INTERNAL_ACTION', [])
    )
    assert any(
        error['category'] == 'missing sequencing kit'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        sequence_file['@id'],
        {
            'sequencing_kit': 'HiSeq Rapid SBS Kit v2'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent sequencing kit'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        sequence_file['@id'],
        {
            'sequencing_kit': 'NovaSeq 6000 S4 Reagent Kit v1.5',
            'sequencing_platform': platform_term_NovaSeq['@id']
        }
    )
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'file_set': measurement_set['@id'],
            'illumina_read_type': 'R2',
            'sequencing_run': 1
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent sequencing kit' and 'and unspecified kit(s)' in error['detail']
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'sequencing_kit': 'NovaSeq 6000 SP Reagent Kit v1.5'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent sequencing kit'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'sequencing_kit': 'NovaSeq 6000 S4 Reagent Kit v1.5',
            'sequencing_platform': platform_term_NovaSeq['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent sequencing kit'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        platform_term_NovaSeq['@id'],
        {
            'sequencing_kits': ['NextSeq 1000/2000 P1 Reagent Kit']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent sequencing kit'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_unexpected_virtual_sample(
    testapp,
    measurement_set,
    tissue
):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [tissue['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected sample'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        tissue['@id'],
        {
            'virtual': True
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected sample'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_missing_auxiliary_set_link(
    testapp,
    measurement_set,
    base_auxiliary_set,
    auxiliary_set_cell_sorting,
    tissue
):
    testapp.patch_json(
        base_auxiliary_set['@id'],
        {
            'samples': [tissue['@id']],
            'status': 'in progress'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing auxiliary set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing auxiliary set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        auxiliary_set_cell_sorting['@id'],
        {
            'samples': [tissue['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing auxiliary set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        auxiliary_set_cell_sorting['@id'],
        {
            'status': 'deleted'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing auxiliary set'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_missing_auxiliary_set_MPRA(
    testapp,
    measurement_set,
    assay_term_mpra,
    base_auxiliary_set,
    auxiliary_set_circularized_RNA
):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_mpra['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing auxiliary set'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        base_auxiliary_set['@id'],
        {
            'file_set_type': 'gRNA sequencing'
        }
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing auxiliary set'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        base_auxiliary_set['@id'],
        {
            'file_set_type': 'quantification DNA barcode sequencing'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing auxiliary set'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'preferred_assay_title': 'MPRA (scQer)'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing auxiliary set'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id'], auxiliary_set_circularized_RNA['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing auxiliary set'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_missing_cell_sorting_auxiliary_set(
    testapp,
    measurement_set,
    assay_term_crispr,
    auxiliary_set_cell_sorting
):
    testapp.patch_json(
        assay_term_crispr['@id'],
        {
            'term_name': 'in vitro CRISPR screen using flow cytometry'
        }
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_crispr['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing auxiliary set'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'auxiliary_sets': [auxiliary_set_cell_sorting['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing auxiliary set'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_missing_auxiliary_set_CRISPR_gRNA_sequencing(
    testapp,
    measurement_set,
    assay_term_crispr,
    base_auxiliary_set
):
    testapp.patch_json(
        assay_term_crispr['@id'],
        {
            'term_name': 'in vitro CRISPR screen using single-cell RNA-seq'
        }
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_crispr['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing auxiliary set'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        base_auxiliary_set['@id'],
        {
            'file_set_type': 'quantification DNA barcode sequencing'
        }
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing auxiliary set'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        base_auxiliary_set['@id'],
        {
            'file_set_type': 'gRNA sequencing'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing auxiliary set'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_missing_auxiliary_set_10x_MULTI_seq(
    testapp,
    measurement_set,
    base_auxiliary_set
):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'preferred_assay_title': '10x multiome with MULTI-seq'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing auxiliary set'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        base_auxiliary_set['@id'],
        {
            'file_set_type': 'lipid-conjugated oligo sequencing'
        }
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing auxiliary set'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_targeted_genes(
    testapp,
    measurement_set,
    assay_term_chip,
    gene_myc_hs
):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_chip['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing targeted genes'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'targeted_genes': [gene_myc_hs['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing targeted genes'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        assay_term_chip['@id'],
        {
            'term_name': 'RNA-seq'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected targeted genes'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_missing_construct_library_set(
    testapp,
    measurement_set,
    tissue,
    assay_term_crispr,
    construct_library_set_genome_wide,
    construct_library_set_editing_template_library
):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_crispr['@id']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing construct library set'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        tissue['@id'],
        {
            'construct_library_sets': [construct_library_set_genome_wide['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing construct library set'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        measurement_set['@id'],
        {
            'preferred_assay_title': 'SGE'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing construct library set'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        tissue['@id'],
        {
            'construct_library_sets': [construct_library_set_editing_template_library['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing construct library set'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_missing_read_names(
    testapp,
    measurement_set_mpra,
    sequence_file
):
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': measurement_set_mpra['@id']
        }
    )
    res = testapp.get(measurement_set_mpra['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing read names'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        sequence_file['@id'],
        {
            'read_names': ['Barcode forward']
        }
    )
    res = testapp.get(measurement_set_mpra['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing read names'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        sequence_file['@id'],
        {
            'read_names': ['Barcode forward', 'Read 1']
        }
    )
    res = testapp.get(measurement_set_mpra['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent read names'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        sequence_file['@id'],
        {
            'read_names': ['Barcode forward', 'Barcode reverse']
        }
    )
    res = testapp.get(measurement_set_mpra['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent read names'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_onlist(testapp, measurement_set_one_onlist, measurement_set, assay_term_scrna, assay_term_mpra):
    # Check if the correct measurement set with onlist info is audit-free
    res = testapp.get(measurement_set_one_onlist['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing barcode onlist'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    # Patch a correct single cell measurement set to be a non-single cell to see if no onlist needed audit shows
    testapp.patch_json(
        measurement_set_one_onlist['@id'],
        {
            'assay_term': assay_term_mpra['@id']
        }
    )
    res = testapp.get(measurement_set_one_onlist['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected barcode onlist'
        for error in res.json['audit'].get('ERROR', [])
    )
    # Check if a non-scRNAseq MeaSet without onlist files and method will trigger warnings.
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing barcode onlist'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    # Patch the basic MeaSet to be scRNAseq without an onlist method or files to trigger audit
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_scrna['@id'],
            'preferred_assay_title': 'SHARE-seq'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing barcode onlist'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_inconsistent_barcode_onlist(testapp, measurement_set_one_onlist, measurement_set_two_onlists, tabular_file_onlist_1, tabular_file_onlist_2):
    # Check the MeaSet with two file and combination method (no audit)
    res = testapp.get(measurement_set_two_onlists['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent barcode onlist'
        for error in res.json['audit'].get('ERROR', [])
    )
    # Patch a MeaSet with 2 onlist files and no combination method (audit).
    testapp.patch_json(
        measurement_set_one_onlist['@id'],
        {
            'onlist_files': [tabular_file_onlist_1['@id'], tabular_file_onlist_2['@id']]
        }
    )
    res = testapp.get(measurement_set_one_onlist['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent barcode onlist'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_unexpected_onlist_files(testapp, measurement_set_one_onlist, tabular_file_onlist_1):
    # Check if the measurement set fixture with one file and no combination method is audit-free
    res = testapp.get(measurement_set_one_onlist['@id'] + '@@audit')
    assert all(
        error['category'] != 'unexpected onlist files'
        for error in res.json['audit'].get('ERROR', [])
    )
    # Check if other content type will trigger warning
    testapp.patch_json(
        tabular_file_onlist_1['@id'],
        {
            'content_type': 'barcode to element mapping'
        }
    )
    res = testapp.get(measurement_set_one_onlist['@id'] + '@@audit')
    assert any(
        error['category'] == 'unexpected onlist files'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_missing_strand_specificity(testapp, measurement_set_perturb_seq):
    # Check if the measurement set with no strand_specificity and preferred assay title Perturb-seq is audited
    res = testapp.get(measurement_set_perturb_seq['@id'] + '@@audit')
    assert all(
        error['category'] == 'missing strand specificity'
        for error in res.json['audit'].get('ERROR', [])
    )
    # Check if other content type will trigger warning
    testapp.patch_json(
        measurement_set_perturb_seq['@id'],
        {
            'strand_specificity': "5' to 3'"
        }
    )
    res = testapp.get(measurement_set_perturb_seq['@id'] + '@@audit')
    assert any(
        error['category'] != 'missing strand specificity'
        for error in res.json['audit'].get('ERROR', [])
    )
