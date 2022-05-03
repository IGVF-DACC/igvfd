import pytest


def test_config_exists():
    from infrastructure.config import config
    assert config['org_name'] == 'igvf-dacc'
