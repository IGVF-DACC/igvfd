import pytest


def test_workflow_upgrade_1_2(upgrader, workflow_v1):
    value = upgrader.upgrade(
        'workflow', workflow_v1,
        current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'publication_identifiers' in value
    assert 'references' not in value
