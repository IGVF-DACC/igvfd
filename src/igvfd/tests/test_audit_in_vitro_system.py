import pytest


def test_audit_in_vitro_system_sorted_fraction(testapp, in_vitro_differentiated_cell_other_product_info_sorted_fraction):
    res = testapp.get(in_vitro_differentiated_cell_other_product_info_sorted_fraction['@id'] + '@@index-data')
    audits = res.json['audit']
    audit_errors = audits.get('ERROR')
    assert audit_errors is not None
    assert len(audit_errors) == 3
    inconsistent_source_count = 0
    inconsistent_product_id_count = 0
    inconsistent_lot_id_count = 0
    for current_audit_error in audit_errors:
        if current_audit_error['category'] == 'sorted fraction inconsistent source':
            inconsistent_source_count += 1
        if current_audit_error['category'] == 'sorted fraction inconsistent product_id':
            inconsistent_product_id_count += 1
        if current_audit_error['category'] == 'sorted fraction inconsistent lot_id':
            inconsistent_lot_id_count += 1
    assert inconsistent_source_count == 1
    assert inconsistent_product_id_count == 1
    assert inconsistent_lot_id_count == 1
