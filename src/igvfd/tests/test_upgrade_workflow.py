import pytest


def test_workflow_upgrade_1_2(upgrader, workflow_v1):
    ids = workflow_v1['references']
    value = upgrader.upgrade(
        'workflow', workflow_v1,
        current_version='1', target_version='2')
    assert value['schema_version'] == '2'
    assert 'publication_identifiers' in value and value['publication_identifiers'] == ids
    assert 'references' not in value


def test_workflow_upgrade_2_3(upgrader, workflow_v2):
    value = upgrader.upgrade(
        'workflow', workflow_v2,
        current_version='2', target_version='3')
    assert value['schema_version'] == '3'
    assert 'description' not in value


def test_workflow_upgrade_4_5(upgrader, workflow_v4):
    value = upgrader.upgrade(
        'workflow', workflow_v4,
        current_version='4', target_version='5')
    assert value['schema_version'] == '5'
    assert 'publication_identifiers' not in value


def test_workflow_upgrade_5_6(upgrader, workflow_v5):
    value = upgrader.upgrade(
        'workflow', workflow_v5,
        current_version='5', target_version='6')
    assert value['schema_version'] == '6'
    assert isinstance(value['workflow_version'], str)
    assert value['workflow_version'] == 'v5.0.0'
