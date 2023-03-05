import pytest


def test_audit_in_vitro_system_sorted_fraction(testapp, lab, award, source, other_source, human_donor, sample_term_K562):
    item_1 = {
        'classification': 'differentiated cell',
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'product_id': 'GR000001',
        'lot_id': 'R00001',
        'taxa': 'Homo sapiens',
        'donors': [human_donor['@id']],
        'biosample_term': sample_term_K562['@id']
    }
    source_cell = testapp.post_json('/in_vitro_system', item_1, status=201).json['@graph'][0]
    item_2 = {
        'classification': 'differentiated cell',
        'award': award['@id'],
        'lab': lab['@id'],
        'source': other_source['@id'],
        'product_id': 'GR000002',
        'lot_id': 'R00002',
        'taxa': 'Homo sapiens',
        'donors': [human_donor['@id']],
        'biosample_term': sample_term_K562['@id'],
        'sorted_fraction': source_cell['@id']
    }
    sorted_fraction_cell = testapp.post_json('/in_vitro_system', item_2, status=201).json['@graph'][0]
    res = testapp.get(sorted_fraction_cell['@id'] + '@@index-data')
    errors = res.json['audit']
    errors_list = []
    for error_type in errors:
        errors_list.extend(errors[error_type])
    assert any(
        error['category'] == 'sorted fraction inconsistent source'
        for error in errors_list)
    assert any(
        error['category'] == 'sorted fraction inconsistent product_id'
        for error in errors_list)
    assert any(
        error['category'] == 'sorted fraction inconsistent lot_id'
        for error in errors_list)
