import pytest


def test_modification_upgrade_1_2(upgrader, modification_missing_cas_sp):
    value = upgrader.upgrade('modification', modification_missing_cas_sp,
                             current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert value['cas_species'] == 'Streptococcus pyogenes (Sp)'
