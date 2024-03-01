import pytest


def test_audit_related_multiome_datasets(
    testapp,
    primary_cell,
    in_vitro_cell_line,
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
    # `samples` should be the same between other datasets in `related_multiome_datasets`
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'samples': [primary_cell['@id'], in_vitro_cell_line['@id']]
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
            'samples': [primary_cell['@id'], in_vitro_cell_line['@id']]
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
            'samples': [primary_cell['@id'], in_vitro_cell_line['@id']]
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


def test_audit_readout(
    testapp,
    measurement_set_mpra,
    assay_term_rna,
    measurement_set_multiome,
    assay_term_mpra
):
    # Screening assays such as CRISPR screen or MPRA must specify readout
    res = testapp.get(measurement_set_mpra['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent readout'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'readout': assay_term_rna['@id']
        }
    )
    res = testapp.get(measurement_set_mpra['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent readout'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )

    # Other "non-screening" assays may not specify readout
    res = testapp.get(measurement_set_multiome['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent readout'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'readout': assay_term_rna['@id']
        }
    )
    res = testapp.get(measurement_set_multiome['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent readout'
        for error in res.json['audit'].get('ERROR', [])
    )

    # Assay term should not be equivalent to readout term
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'readout': assay_term_mpra['@id']
        }
    )
    res = testapp.get(measurement_set_mpra['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent readout'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_modifications(
    testapp,
    measurement_set,
    in_vitro_cell_line,
    in_vitro_organoid,
    modification,
):
    # No modifications audits on measurement set with no samples
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent modifications'
        for error in res.json['audit'].get('ERROR', [])
    )
    # Modifications should be the same on samples in any measurement set
    testapp.patch_json(
        measurement_set['@id'],
        {
            'samples': [in_vitro_cell_line['@id'], in_vitro_organoid['@id']]
        }
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'modifications': [modification['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent modifications'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_missing_modification(
    testapp,
    measurement_set,
    assay_term_crispr,
    tissue,
    modification_activation
):
    # CRISPR screens must also have modifications on all their samples
    testapp.patch_json(
        measurement_set['@id'],
        {
            'assay_term': assay_term_crispr['@id'],
            'preferred_assay_title': '10x multiome'
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
            'modifications': [modification_activation['@id']]
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
        error['category'] == 'NTR treatment term ID'
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
            'assay_term': assay_term_starr['@id'],
            'preferred_assay_title': 'SUPERSTARR'
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent assays'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        assay_term_starr['@id'],
        {
            'preferred_assay_titles': ['SUPERSTARR']
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent assays'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_inconsistent_institutional_certification(
    testapp,
    measurement_set,
    assay_term_mpra,
    other_lab,
    tissue,
    human_donor,
    assay_term_chip,
    institutional_certificate
):
    # No audit when there are no associated human donors.
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing nih certification'
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
        error['category'] != 'missing nih certification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
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
        error['category'] == 'missing nih certification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )

    # No flag if the NIC's lab and award match the Measurement Set.
    testapp.patch_json(
        institutional_certificate['@id'],
        {
            'samples': [tissue['@id']]
        }
    )
    res = testapp.get(measurement_set['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing nih certification'
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
        error['category'] == 'missing nih certification'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )


def test_audit_missing_seqspec(
    testapp,
    measurement_set,
    sequence_file,
    configuration_file_seqspec
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
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
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
    configuration_file_seqspec_2
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
    # sequence files from different sequencing runs should not link to the same seqspec
    testapp.patch_json(
        sequence_file_sequencing_run_2['@id'],
        {
            'sequencing_run': 2
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
