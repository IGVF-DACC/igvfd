import pytest


def test_image_file_upgrade_3_4(upgrader, image_file_v3):
    value = upgrader.upgrade('image_file', image_file_v3, current_version='3', target_version='4')
    assert 'derived_from' not in value
    assert 'file_format_specifications' not in value
    assert value['schema_version'] == '4'
