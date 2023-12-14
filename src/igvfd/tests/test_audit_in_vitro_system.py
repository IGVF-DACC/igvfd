import pytest


def test_audit_targeted_sample_term(
    testapp,
    in_vitro_cell_line,
    sample_term_K562
):
    # In vitro systems should not have the same sample_term specified in targeted_sample_term and sample_terms.
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'targeted_sample_term': sample_term_K562['@id']}
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent targeted_sample_term'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_targeted_sample_term(
    testapp,
    in_vitro_cell_line,
    treatment_chemical,
    treatment_protein
):
    # Treatments in cell_fate_change_treatments should not be of purpose "perturbation", "agonist", "antagonist", or "control".
    testapp.patch_json(
        treatment_chemical['@id'],
        {
            'purpose': 'perturbation'
        }
    )
    testapp.patch_json(
        treatment_protein['@id'],
        {
            'purpose': 'control'
        }
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'cell_fate_change_treatments': [treatment_chemical['@id'], treatment_protein['@id']],
            'time_post_change': 5,
            'time_post_change_units': 'minute'
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent cell_fate_change_treatments treatment purpose'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        treatment_chemical['@id'],
        {
            'purpose': 'differentiation'
        }
    )
    testapp.patch_json(
        treatment_protein['@id'],
        {
            'purpose': 'de-differentiation'
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent cell_fate_change_treatments treatment purpose'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_cell_fate_change_protocol_document_type(
    testapp,
    in_vitro_cell_line,
    sample_term_brown_adipose_tissue,
    experimental_protocol_document
):
    # A document linked in cell_fate_change_protocol should be document_type cell fate change protocol
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'classification': 'organoid',
            'time_post_change': 5,
            'time_post_change_units': 'minute',
            'targeted_sample_term': sample_term_brown_adipose_tissue['@id'],
            'cell_fate_change_protocol': experimental_protocol_document['@id']
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent cell_fate_change_protocol document type'
        for error in res.json['audit'].get('ERROR', [])
    )

    testapp.patch_json(
        experimental_protocol_document['@id'],
        {
            'document_type': 'cell fate change protocol'
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent cell_fate_change_protocol document type'
        for error in res.json['audit'].get('ERROR', [])
    )
