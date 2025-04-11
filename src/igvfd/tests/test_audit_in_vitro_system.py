import pytest


def test_audit_targeted_sample_term(
    testapp,
    in_vitro_cell_line,
    sample_term_K562,
    experimental_protocol_document
):
    # In vitro systems should not have the same sample_term specified in targeted_sample_term and sample_terms.
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {'targeted_sample_term': sample_term_K562['@id'],
         'cell_fate_change_protocol': experimental_protocol_document['@id'],
         'time_post_change': 10,
         'time_post_change_units': 'minute',
         'classifications': ['differentiated cell specimen']}
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent targeted sample term'
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
            'classifications': ['organoid'],
            'time_post_change': 5,
            'time_post_change_units': 'minute',
            'targeted_sample_term': sample_term_brown_adipose_tissue['@id'],
            'cell_fate_change_protocol': experimental_protocol_document['@id']
        }
    )
    res = testapp.get(in_vitro_cell_line['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent document type'
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
        error['category'] != 'inconsistent document type'
        for error in res.json['audit'].get('ERROR', [])
    )
