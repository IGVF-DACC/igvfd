import pytest


def test_whole_organism_upgrade1(upgrader, whole_organism_1):
    value = upgrader.upgrade('whole_organism', whole_organism_1, current_version='1', target_version='2')
    assert value['schema_version'] == '2'
