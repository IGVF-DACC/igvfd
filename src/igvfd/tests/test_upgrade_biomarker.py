import pytest


def test_biomarker_upgrade_1_2(upgrader, biomarker_v1):
    alias = biomarker_v1['aliases']
    synonym = biomarker_v1['synonyms']
    value = upgrader.upgrade('biomarker', biomarker_v1, current_version='1', target_version='2')
    assert 'aliases' not in value
    assert alias == value['alias']
    assert 'synonyms' not in value
    assert synonym == value['synonym']
    assert value['schema_version'] == '2'
