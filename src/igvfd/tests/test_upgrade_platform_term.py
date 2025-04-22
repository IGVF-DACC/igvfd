import pytest


def test_platform_term_upgrade_1_2(upgrader, platform_term_v1):
    value = upgrader.upgrade('platform_term', platform_term_v1, current_version='1', target_version='2')
    assert 'description' not in value
    assert value['schema_version'] == '2'


def test_platform_term_upgrade_3_4(upgrader, platform_term_v3):
    value = upgrader.upgrade('platform_term', platform_term_v3, current_version='3', target_version='4')
    assert 'NovaSeq 6000 S4 Reagent Kit V1.5' not in value['sequencing_kits']
    assert 'NovaSeq 6000 S4 Reagent Kit v1.5' in value['sequencing_kits']
    assert value['schema_version'] == '4'


def test_platform_term_upgrade_4_5(upgrader, platform_term_v4):
    value = upgrader.upgrade('platform_term', platform_term_v4, current_version='4', target_version='5')
    assert 'definition' not in value
    assert 'comment' not in value
    assert value['schema_version'] == '5'
