import pytest


def test_page_upgrade_2_3(upgrader, page_v2):
    value = upgrader.upgrade('page', page_v2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'
