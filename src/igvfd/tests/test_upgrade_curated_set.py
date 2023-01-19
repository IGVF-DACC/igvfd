import pytest


def test_curated_set_upgrade_1_2(upgrader, curated_set_v1):
    samples = curated_set_v1['sample']
    donors = curated_set_v1['donor']
    value = upgrader.upgrade('curated_set', curated_set_v1, current_version='1', target_version='2')
    assert 'sample' not in value
    assert samples == value['samples']
    assert 'donor' not in value
    assert donors == value['donors']
    assert value['schema_version'] == '2'
