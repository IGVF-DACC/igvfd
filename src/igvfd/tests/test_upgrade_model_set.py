import pytest


def test_model_set_upgrade_1_2(upgrader, model_set_v1):
    value = upgrader.upgrade('model_set', model_set_v1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'description' not in value


def test_model_set_upgrade_3_4(upgrader, model_set_v3):
    value = upgrader.upgrade('model_set', model_set_v3, current_version='3', target_version='4')
    assert value['schema_version'] == '4'
    assert 'publication_identifiers' not in value


def test_model_set_upgrade_4_5(upgrader, model_set_v4):
    value = upgrader.upgrade('model_set', model_set_v4, current_version='4', target_version='5')
    assert value['schema_version'] == '5'
    assert 'software_version' not in value


def test_model_set_upgrade_5_6(upgrader, model_set_v5, model_set_v5_2):
    value = upgrader.upgrade('model_set', model_set_v5, current_version='5', target_version='6')
    assert value['schema_version'] == '6'
    assert value.get('preferred_assay_titles') == ['10x snATAC-seq with Scale pre-indexing']
    assert value.get('notes') == 'This model set previously used 10x with Scale pre-indexing as a preferred_assay_titles, but it has been updated to 10x snATAC-seq with Scale pre-indexing via an upgrade.'
    value = upgrader.upgrade('model_set', model_set_v5_2, current_version='5', target_version='6')
    assert value['schema_version'] == '6'
    assert value.get('preferred_assay_titles') == ['Perturb-seq']


def test_model_set_upgrade_6_7(upgrader, model_set_v6):
    value = upgrader.upgrade('model_set', model_set_v6, current_version='6', target_version='7')
    assert value['schema_version'] == '7'
    assert value.get('assay_terms') == ['/assay-terms/OBI_0002041/']
    assert 'This model set assay_terms was defaulted to /assay-terms/OBI_0002041/ via an upgrade, update with appropriate assay_terms if needed.' in value.get(
        'notes', '')
