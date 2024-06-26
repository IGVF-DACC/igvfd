import pytest


def test_modification_upgrade_1_2(upgrader, modification_missing_cas_sp):
    value = upgrader.upgrade('modification', modification_missing_cas_sp,
                             current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert value['cas_species'] == 'Streptococcus pyogenes (Sp)'
    assert 'For upgrade, cas_species has been automatically designated as Streptococcus pyogenes (Sp), follow up with associated lab to check if upgrade is valid.' in value[
        'notes']


def test_modification_upgrade_2_3(upgrader, modification_v2):
    sources = [modification_v2['source']]
    value = upgrader.upgrade('modification', modification_v2, current_version='2', target_version='3')
    assert 'source' not in value
    assert sources == value['sources']
    assert type(value['sources']) == list
    assert value['schema_version'] == '3'


def test_modification_upgrade_3_4(upgrader, modification_v3):
    value = upgrader.upgrade('modification', modification_v3, current_version='3', target_version='4')
    assert value['schema_version'] == '4'
    assert 'description' not in value


def test_modification_upgrade_5_6(upgrader, modification_v5):
    value = upgrader.upgrade('modification', modification_v5, current_version='5', target_version='6')
    assert value['schema_version'] == '6'
    assert value['fused_doamin'] == 'ZIM3-KRAB'
