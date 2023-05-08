import pytest


def test_in_vitro_system_upgrade_1_2(upgrader, in_vitro_system_v1):
    assert 'donor' in in_vitro_system_v1
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v1, current_version='1', target_version='2')
    assert 'donor' not in value
    assert 'donors' in value
    assert value['schema_version'] == '2'


def test_in_vitro_system_upgrade_2_3(upgrader, in_vitro_system_v2):
    biomarkers = in_vitro_system_v2['biomarker']
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v2, current_version='2', target_version='3')
    assert 'biomarker' not in value
    assert biomarkers == value['biomarkers']
    assert value['schema_version'] == '3'


def test_in_vitro_system_upgrade_3_4(upgrader, in_vitro_system_v3):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v3, current_version='3', target_version='4')
    assert value['accession'] == 'IGVFSM0222IIVA'
    assert value['schema_version'] == '4'


def test_in_vitro_system_upgrade_4_5(upgrader, in_vitro_system_v4):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v4, current_version='4', target_version='5')
    assert value['schema_version'] == '5'
    assert value.get('classification') == 'organoid'


def test_in_vitro_system_upgrade_5_6(upgrader, in_vitro_system_v5):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v5, current_version='5', target_version='6')
    assert value['schema_version'] == '6'
    assert value['sorted_fraction_detail'] == 'Default upgrade text: please add more details about sorted_fraction, see sample.json for description.'


def test_in_vitro_system_upgrade_6_7(upgrader, in_vitro_system_v6):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v6, current_version='6', target_version='7')
    assert value['schema_version'] == '7'
    assert value['taxa'] != 'Saccharomyces'
    assert value['notes'] == 'Previous taxa: Saccharomyces is no longer valid.'


def test_in_vitro_system_upgrade_7_8(upgrader, in_vitro_system_v7):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v7, current_version='7', target_version='8')
    assert value['schema_version'] == '8'
    assert value['classification'] == 'differentiated cell specimen'


def test_in_vitro_system_upgrade_8_9(upgrader, in_vitro_system_v8):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v8, current_version='8', target_version='9')
    assert value['schema_version'] == '9'
    assert 'taxa' not in value
    assert value['notes'] == 'Test.  Previous taxa: Homo sapiens will now be calculated.'


def test_in_vitro_system_upgrade_8_9(upgrader, in_vitro_system_v8_1, in_vitro_system_v8_2):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v8_1, current_version='8', target_version='9')
    assert value['schema_version'] == '9'
    assert 'time_post_factors_introduction' not in in_vitro_system_v8_1 and 'time_post_factors_introduction_units' not in in_vitro_system_v8_1
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v8_2, current_version='8', target_version='9')
    assert value['schema_version'] == '9'
    assert 'introduced_factors' not in in_vitro_system_v8_2
