import pytest


def test_modification_upgrade_1_2(upgrader, modification):
    value = upgrader.upgrade('modification', modification,
                             current_version='1', target_version='2')
    assert value['schema_version'] == '1'
    assert value.get('cas_species') == 'Streptococcus pyogenes (Sp)'
