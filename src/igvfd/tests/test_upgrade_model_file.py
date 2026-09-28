import pytest


def test_model_file_upgrade_2_3(upgrader, model_file_v2):
    catalog_adapters = model_file_v2['catalog_adapters']
    value = upgrader.upgrade('model_file', model_file_v2, current_version='2', target_version='3')
    assert 'catalog_adapters' not in value
    assert value['schema_version'] == '3'
    assert value['notes'].endswith(
        f"This file's catalog_adapters was {catalog_adapters}, and was removed via upgrade.")
