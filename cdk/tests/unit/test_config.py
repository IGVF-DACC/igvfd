import pytest


def test_config_exists():
    from infrastructure.config import config
    assert 'demo' in config['environment']
    assert 'demo' in config['pipeline']


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
        postgres={},
        opensearch={},
        backend={},
        invalidation_service={},
        indexing_service={},
        tags=[
            ('abc', '123'),
            ('xyz', '321'),
        ]
    )
    assert config.common.organization_name == 'igvf-dacc'
    assert config.common.project_name == 'igvfd'
    assert config.postgres == {}
    assert config.opensearch == {}
    assert config.backend == {}
    assert config.invalidation_service == {}
    assert config.indexing_service == {}
    assert config.branch == 'xyz-branch'
    assert config.tags == [
        ('abc', '123'),
        ('xyz', '321'),
    ]


def test_config_pipeline_config_dataclass():
    from infrastructure.config import PipelineConfig
    from infrastructure.constructs.existing import igvf_dev
    config = PipelineConfig(
        name='demo',
        branch='xyz-branch',
        pipeline='xyz-pipeline',
        existing_resources_class=igvf_dev.Resources,
        account_and_region=igvf_dev.US_WEST_2,
        tags=[
            ('abc', '123'),
            ('xyz', '321'),
        ]
    )
    assert config.common.organization_name == 'igvf-dacc'
    assert config.common.project_name == 'igvfd'
    assert config.existing_resources_class == igvf_dev.Resources
    assert config.account_and_region == igvf_dev.US_WEST_2
    assert config.branch == 'xyz-branch'
    assert config.pipeline == 'xyz-pipeline'
    assert config.tags == [
        ('abc', '123'),
        ('xyz', '321'),
    ]


def test_config_build_config_from_name():
    from infrastructure.config import build_config_from_name
    from infrastructure.constants import DEV_DATABASE_IDENTIFIER
    config = build_config_from_name(
        'demo',
        branch='my-branch',
    )
    assert config.common.organization_name == 'igvf-dacc'
    assert config.common.project_name == 'igvfd'
    postgres_instance_props = config.postgres['instances'][0]['props']
    assert (
        'snapshot_source_db_identifier' in postgres_instance_props
        or 'snapshot_arn' in postgres_instance_props
    )
    opensearch_instance_props = config.opensearch['clusters'][0]['props']
    assert 'capacity' in opensearch_instance_props
    assert 'volume_size' in opensearch_instance_props
    assert 'cpu' in config.invalidation_service
    assert 'memory_limit_mib' in config.invalidation_service
    assert 'min_scaling_capacity' in config.invalidation_service
    assert 'max_scaling_capacity' in config.invalidation_service
    assert 'cpu' in config.indexing_service
    assert 'memory_limit_mib' in config.indexing_service
    assert 'min_scaling_capacity' in config.indexing_service
    assert 'max_scaling_capacity' in config.indexing_service
    assert config.branch == 'my-branch'
    assert config.name == 'demo'
    config = build_config_from_name(
        'dev',
        branch='my-branch',
        tags=[
            ('some', 'override')
        ]
    )
    assert config.common.organization_name == 'igvf-dacc'
    assert config.common.project_name == 'igvfd'
    assert config.tags == [
        ('some', 'override')
    ]
    postgres_instance_props = config.postgres['instances'][0]['props']
    assert (
        'snapshot_source_db_identifier' in postgres_instance_props
        and 'snapshot_arn' not in postgres_instance_props
    )
    opensearch_instance_props = config.opensearch['clusters'][0]['props']
    assert 'capacity' in opensearch_instance_props
    assert 'volume_size' in opensearch_instance_props
    assert 'cpu' in config.invalidation_service
    assert 'memory_limit_mib' in config.invalidation_service
    assert 'min_scaling_capacity' in config.invalidation_service
    assert 'max_scaling_capacity' in config.invalidation_service
    assert 'cpu' in config.indexing_service
    assert 'memory_limit_mib' in config.indexing_service
    assert 'min_scaling_capacity' in config.indexing_service
    assert 'max_scaling_capacity' in config.indexing_service
    assert config.branch == 'my-branch'
    assert config.name == 'dev'


def test_config_build_pipeline_config_from_name():
    from aws_cdk import Environment
    from infrastructure.constructs.existing import igvf_dev
    from infrastructure.config import build_pipeline_config_from_name
    config = build_pipeline_config_from_name(
        'demo',
        branch='my-branch',
        pipeline='my-pipeline',
    )
    assert config.common.organization_name == 'igvf-dacc'
    assert config.common.project_name == 'igvfd'
    assert ('time-to-live-hours', '72') in config.tags
    assert config.branch == 'my-branch'
    assert config.pipeline == 'my-pipeline'
    assert config.name == 'demo'
    config = build_pipeline_config_from_name(
        'dev',
        branch='my-branch',
    )
    assert config.common.organization_name == 'igvf-dacc'
    assert config.common.project_name == 'igvfd'
    assert config.pipeline == 'ContinuousDeploymentPipelineStack'
    assert config.name == 'dev'
    assert isinstance(config.account_and_region, Environment)
    assert config.existing_resources_class == igvf_dev.Resources


def test_config_get_config_name_from_branch():
    from infrastructure.config import get_config_name_from_branch
    config_name = get_config_name_from_branch('IGVF-123-add-new-feature')
    assert config_name == 'demo'
    config_name = get_config_name_from_branch('dev')
    assert config_name == 'dev'


def test_config_get_pipeline_config_name_from_branch():
    from infrastructure.config import get_pipeline_config_name_from_branch
    config_name = get_pipeline_config_name_from_branch('IGVF-123-add-new-feature')
    assert config_name == 'demo'
    config_name = get_pipeline_config_name_from_branch('dev')
    assert config_name == 'dev'
    config_name = get_pipeline_config_name_from_branch('main')
    assert config_name == 'production'
