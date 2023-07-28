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


def test_curated_set_upgrade_2_3(upgrader, curated_set_v2):
    value = upgrader.upgrade('curated_set', curated_set_v2, current_version='2', target_version='3')
    assert value['accession'] == 'IGVFDS0000ZZZA'
    assert value['schema_version'] == '3'


def test_curated_set_upgrade_3_4(upgrader, curated_set_v3):
    ids = curated_set_v3['identifiers']
    value = upgrader.upgrade(
        'curated_set', curated_set_v3,
        current_version='3', target_version='4')
    assert value['schema_version'] == '4'
    assert 'publication_identifiers' in value and value['publication_identifiers'] == ids
    assert 'references' not in value
