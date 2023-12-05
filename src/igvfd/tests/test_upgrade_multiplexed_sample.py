import pytest


def test_multiplexed_sample_upgrade_1_2(upgrader, multiplexed_sample_v1):
    value = upgrader.upgrade('multiplexed_sample', multiplexed_sample_v1, current_version='1', target_version='2')
    assert 'source' not in value
    assert 'product_id' not in value
    assert 'lot_id' not in value
    assert value['notes'] == 'Source /sources/sigma/ was removed via upgrade. Product ID ab272168 was removed via upgrade. Lot ID 0000001 was removed via upgrade.'
    assert value['schema_version'] == '2'


def test_multiplexed_sample_upgrade_2_3(upgrader, multiplexed_sample_v2):
    value = upgrader.upgrade('multiplexed_sample', multiplexed_sample_v2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'


def test_multiplexed_sample_3_4(upgrader, multiplexed_sample_v3_no_units, multiplexed_sample_v3_no_amount):
    value = upgrader.upgrade('multiplexed_sample', multiplexed_sample_v3_no_units,
                             current_version='3', target_version='4')
    assert 'starting_amount_units' in value and value['starting_amount_units'] == 'items'
    assert value['schema_version'] == '4'
    value = upgrader.upgrade('multiplexed_sample', multiplexed_sample_v3_no_amount,
                             current_version='3', target_version='4')
    assert 'starting_amount' in value and value['starting_amount'] == 0
    assert value['schema_version'] == '4'


def test_multiplexed_sample_upgrade_4_5(upgrader, multiplexed_sample_v4):
    sorted_sample = multiplexed_sample_v4['sorted_fraction']
    sorted_sample_detail = multiplexed_sample_v4['sorted_fraction_detail']
    value = upgrader.upgrade('multiplexed_sample', multiplexed_sample_v4, current_version='4', target_version='5')
    assert 'sorted_from' in value and value['sorted_from'] == sorted_sample
    assert 'sorted_from_detail' in value and value['sorted_from_detail'] == sorted_sample_detail
    assert value['schema_version'] == '5'


def test_multiplexed_sample_upgrade_5_6(upgrader, multiplexed_sample_v5):
    value = upgrader.upgrade('multiplexed_sample', multiplexed_sample_v5, current_version='5', target_version='6')
    assert value['schema_version'] == '6'
    assert 'description' not in value
