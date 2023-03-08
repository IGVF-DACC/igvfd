import pytest


def test_audit_in_vitro_system_sorted_fraction(testapp, in_vitro_differentiated_cell, in_vitro_differentiated_cell_other_product_info_sorted_fraction):
    res = testapp.get(in_vitro_differentiated_cell_other_product_info_sorted_fraction['@id'] + '@@index-data')
    audits = res.json['audit']
    audit_error_list = audits.get('ERROR')
    assert audit_error_list is not None
    assert len(audit_error_list) == 1
    audit_error = audit_error_list[0]
    assert audit_error['category'] == 'sorted fraction inconsistent'
    detail_msg = 'Sample {'
    detail_msg += in_vitro_differentiated_cell_other_product_info_sorted_fraction['accession']
    detail_msg += '|'
    detail_msg += in_vitro_differentiated_cell_other_product_info_sorted_fraction['@id']
    detail_msg += '} is different from the associated parent sample {'
    detail_msg += in_vitro_differentiated_cell['accession']
    detail_msg += '|'
    detail_msg += in_vitro_differentiated_cell['@id']
    detail_msg += '} because the following properties are different: lot_id, source, product_id'
    assert audit_error['detail'] == detail_msg
