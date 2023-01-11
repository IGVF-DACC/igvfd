import pytest


def test_in_vitro_system_upgrade_1_2(upgrader, in_vitro_differentiated_tissue):
    value = upgrader.upgrade('cell_line', in_vitro_differentiated_tissue, current_version='1', target_version='2')
    assert 'donor' not in value
    assert value['schema_version'] == '2'
