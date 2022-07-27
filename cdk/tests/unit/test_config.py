import pytest


def test_config_exists():
    from infrastructure.config import config
    assert 'demo' in config['environment']


def test_config_common_dataclass():
    from infrastructure.config import Common
    common = Common()
    assert common.organization_name == 'igvf-dacc'
    assert common.project_name == 'igvfd'


def test_config_config_dataclass():
    from infrastructure.config import Config
    config = Config(
        name='demo',
        branch='xyz-branch',
        pipeline='xyz-pipeline',
    )
    assert config.common.organization_name == 'igvf-dacc'
    assert config.common.project_name == 'igvfd'
    assert config.snapshot_source_db_identifier is None
    assert config.branch == 'xyz-branch'
    assert config.pipeline == 'xyz-pipeline'


def test_config_build_config_from_name():
    from infrastructure.config import build_config_from_name
    from infrastructure.constants import DEV_DATABASE_IDENTIFIER
    config = build_config_from_name(
        'demo',
        branch='my-branch',
        pipeline='my-pipeline',
    )
    assert config.common.organization_name == 'igvf-dacc'
    assert config.common.project_name == 'igvfd'
    assert config.snapshot_source_db_identifier or config.snapshot_arn
    assert config.branch == 'my-branch'
    assert config.pipeline == 'my-pipeline'
    assert config.name == 'demo'
    config = build_config_from_name(
        'demo',
        branch='my-branch',
        # Overrides.
        pipeline='my-pipeline',
    )
    config = build_config_from_name(
        'dev',
        branch='my-branch',
    )
    assert config.common.organization_name == 'igvf-dacc'
    assert config.common.project_name == 'igvfd'
    assert config.snapshot_source_db_identifier is None
    assert config.branch == 'my-branch'
    assert config.pipeline == 'ContinuousDeploymentPipelineStack'
    assert config.name == 'dev'


def test_config_build_config_from_branch():
    from infrastructure.config import get_config_name_from_branch
    config_name = get_config_name_from_branch('IGVF-123-add-new-feature')
    assert config_name == 'demo'
    config_name = get_config_name_from_branch('dev')
    assert config_name == 'dev'
