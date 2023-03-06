import pytest


def test_audit_whole_organism(testapp, lab, award, source, other_source, rodent_donor, sample_term_whole_organism, sample_term_K562, phenotype_term_alzheimers):
    item_1 = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id'],
        'taxa': 'Mus musculus',
        'donors': [rodent_donor['@id']],
        'biosample_term': sample_term_whole_organism['@id']
    }
    source_whole_organism = testapp.post_json('/whole_organism', item_1, status=201).json['@graph'][0]
    item_2 = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': other_source['@id'],
        'taxa': 'Mus musculus',
        'donors': [rodent_donor['@id']],
        'biosample_term': sample_term_K562['@id'],
        'sorted_fraction': source_whole_organism['@id'],
        'collections': ['ENCODE'],
        'disease_terms': [phenotype_term_alzheimers['@id']],
        'embryonic': True
    }
    sorted_fraction_whole_organism = testapp.post_json('/whole_organism', item_2, status=201).json['@graph'][0]
    res = testapp.get(sorted_fraction_whole_organism['@id'] + '@@index-data')
    errors = res.json['audit']
    errors_list = []
    for error_type in errors:
        errors_list.extend(errors[error_type])
    assert any(
        error['category'] == 'sorted fraction inconsistent source'
        for error in errors_list)
    assert any(
        error['category'] == 'sorted fraction parent missing collections'
        for error in errors_list)
    assert any(
        error['category'] == 'sorted fraction parent missing embryonic'
        for error in errors_list)
