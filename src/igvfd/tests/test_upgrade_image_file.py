import pytest


def test_image_file_upgrade_3_4(upgrader, image_file_v3):
    value = upgrader.upgrade('image_file', image_file_v3, current_version='3', target_version='4')
    assert 'derived_from' not in value
    assert 'file_format_specifications' not in value
    assert value['schema_version'] == '4'


def test_image_file_upgrade_5_6(upgrader, image_file_v5):
    value = upgrader.upgrade('image_file', image_file_v5, current_version='5', target_version='6')
    assert value['schema_version'] == '6'
    assert value['release_timestamp'] == '2025-06-24T12:34:56Z'
    assert value['notes'] == "This object's release_timestamp has been set to 2025-06-24T12:34:56Z"
