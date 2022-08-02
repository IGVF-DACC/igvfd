import pytest


def test_assay_term_upgrade_1_2(upgrader, assay_term_v1):
    value = upgrader.upgrade('assay_term', assay_term_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert value['schema_version'] == '2'
