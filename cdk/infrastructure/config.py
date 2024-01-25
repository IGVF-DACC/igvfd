from aws_cdk import Environment

from aws_cdk.aws_ec2 import InstanceType
from aws_cdk.aws_ec2 import InstanceClass
from aws_cdk.aws_ec2 import InstanceSize

from aws_cdk.aws_opensearchservice import CapacityConfig
from aws_cdk.aws_opensearchservice import EngineVersion

from dataclasses import dataclass
from dataclasses import field

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from infrastructure.constants import DEV_DATABASE_IDENTIFIER
from infrastructure.constants import PROD_DATABASE_IDENTIFIER

from infrastructure.constructs.existing import igvf_dev
from infrastructure.constructs.existing import igvf_prod

from infrastructure.constructs.existing.types import ExistingResourcesClass


config: Dict[str, Any] = {
    'pipeline': {
        'demo': {
            'pipeline': 'DemoDeploymentPipelineStack',
            'existing_resources_class': igvf_dev.Resources,
            'account_and_region': igvf_dev.US_WEST_2,
            'tags': [
                ('time-to-live-hours', '60'),
                ('turn-off-on-friday-night', 'yes'),
            ],
        },
        'dev': {
            'pipeline': 'ContinuousDeploymentPipelineStack',
            'existing_resources_class': igvf_dev.Resources,
            'account_and_region': igvf_dev.US_WEST_2,
            'tags': [
            ],
        },
        'production': {
            'pipeline': 'ProductionDeploymentPipelineStack',
            'cross_account_keys': True,
            'existing_resources_class': igvf_prod.Resources,
            'account_and_region': igvf_prod.US_WEST_2,
            'tags': [
            ],
        },
    },
    'environment': {
        'demo': {
            'postgres': {
                'instances': [
                    {
                        'construct_id': 'Postgres',
                        'on': True,
                        'props': {
                            'snapshot_source_db_identifier': DEV_DATABASE_IDENTIFIER,
                            'allocated_storage': 10,
                            'max_allocated_storage': 20,
                            'instance_type': InstanceType.of(
                                InstanceClass.BURSTABLE3,
                                InstanceSize.MEDIUM,
                            ),
                        },
                    }
                ],
            },
            'opensearch': {
                'clusters': [
                    {
                        'construct_id': 'Opensearch27',
                        'on': True,
                        'props': {
                            'capacity': CapacityConfig(
                                data_node_instance_type='m6g.xlarge.search',
                                data_nodes=1,
                            ),
                            'engine_version': EngineVersion.OPENSEARCH_2_7,
                            'volume_size': 30,
                            'logging': False,
                        }
                    }
                ],
            },
            'feature_flag_service': {
                'flags': {
                    'block_database_writes': False,
                }
            },
            'backend': {
                'cpu': 2048,
                'memory_limit_mib': 4096,
                'desired_count': 1,
                'max_capacity': 4,
                'ini_name': 'demo.ini',
                'use_postgres_named': 'Postgres',
                'read_from_opensearch_named': 'Opensearch27',
                'write_to_opensearch_named': 'Opensearch27',
            },
            'invalidation_service': {
                'cpu': 256,
                'memory_limit_mib': 512,
                'min_scaling_capacity': 1,
                'max_scaling_capacity': 2,
            },
            'indexing_service': {
                'cpu': 256,
                'memory_limit_mib': 512,
                'min_scaling_capacity': 1,
                'max_scaling_capacity': 4,
            },
            'tags': [
                ('time-to-live-hours', '60'),
                ('turn-off-on-friday-night', 'yes'),
            ],
        },
        'dev': {
            'postgres': {
                'instances': [
                    {
                        'construct_id': 'Postgres',
                        'on': True,
                        'props': {
                            'snapshot_arn': 'arn:aws:rds:us-west-2:109189702753:snapshot:manual-dev-10-26-23',
                            'allocated_storage': 10,
                            'max_allocated_storage': 20,
                            'instance_type': InstanceType.of(
                                InstanceClass.BURSTABLE3,
                                InstanceSize.MEDIUM,
                            ),
                        },
                    },
                ],
            },
            'opensearch': {
                'clusters': [
                    {
                        'construct_id': 'Opensearch27',
                        'on': True,
                        'props': {
                            'capacity': CapacityConfig(
                                data_node_instance_type='m6g.xlarge.search',
                                data_nodes=1,
                            ),
                            'engine_version': EngineVersion.OPENSEARCH_2_7,
                            'volume_size': 30,
                        }
                    },
                ],
            },
            'feature_flag_service': {
                'flags': {
                    'block_database_writes': False,
                }
            },
            'backend': {
                'cpu': 2048,
                'memory_limit_mib': 4096,
                'desired_count': 1,
                'max_capacity': 4,
                'ini_name': 'demo.ini',
                'use_postgres_named': 'Postgres',
                'read_from_opensearch_named': 'Opensearch27',
                'write_to_opensearch_named': 'Opensearch27',
            },
            'invalidation_service': {
                'cpu': 256,
                'memory_limit_mib': 512,
                'min_scaling_capacity': 1,
                'max_scaling_capacity': 2,
            },
            'indexing_service': {
                'cpu': 256,
                'memory_limit_mib': 512,
                'min_scaling_capacity': 1,
                'max_scaling_capacity': 4,
            },
            'tags': [
            ]
        },
        'staging': {
            'postgres': {
                'instances': [
                    {
                        'construct_id': 'Postgres',
                        'on': True,
                        'props': {
                            'snapshot_source_db_identifier': PROD_DATABASE_IDENTIFIER,
                            'allocated_storage': 10,
                            'max_allocated_storage': 20,
                            'instance_type': InstanceType.of(
                                InstanceClass.BURSTABLE3,
                                InstanceSize.MEDIUM,
                            ),
                        },
                    },
                ],
            },
            'opensearch': {
                'clusters': [
                    {
                        'construct_id': 'Opensearch27',
                        'on': True,
                        'props': {
                            'capacity': CapacityConfig(
                                data_node_instance_type='m6g.xlarge.search',
                                data_nodes=1,
                            ),
                            'engine_version': EngineVersion.OPENSEARCH_2_7,
                            'volume_size': 30,
                        }
                    },
                ],
            },
            'feature_flag_service': {
                'flags': {
                    'block_database_writes': False,
                }
            },
            'backend': {
                'cpu': 2048,
                'memory_limit_mib': 4096,
                'desired_count': 1,
                'max_capacity': 4,
                'ini_name': 'staging.ini',
                'use_postgres_named': 'Postgres',
                'read_from_opensearch_named': 'Opensearch27',
                'write_to_opensearch_named': 'Opensearch27',
            },
            'invalidation_service': {
                'cpu': 256,
                'memory_limit_mib': 512,
                'min_scaling_capacity': 1,
                'max_scaling_capacity': 2,
            },
            'indexing_service': {
                'cpu': 256,
                'memory_limit_mib': 512,
                'min_scaling_capacity': 1,
                'max_scaling_capacity': 4,
            },
            'tags': [
            ],
            'url_prefix': 'api',
        },
        'sandbox': {
            'postgres': {
                'instances': [
                    {
                        'construct_id': 'Postgres',
                        'on': True,
                        'props': {
                            'snapshot_source_db_identifier': PROD_DATABASE_IDENTIFIER,
                            'allocated_storage': 10,
                            'max_allocated_storage': 20,
                            'instance_type': InstanceType.of(
                                InstanceClass.BURSTABLE3,
                                InstanceSize.MEDIUM,
                            ),
                        },
                    },
                ],
            },
            'opensearch': {
                'clusters': [
                    {
                        'construct_id': 'Opensearch27',
                        'on': True,
                        'props': {
                            'capacity': CapacityConfig(
                                data_node_instance_type='m6g.xlarge.search',
                                data_nodes=1,
                            ),
                            'engine_version': EngineVersion.OPENSEARCH_2_7,
                            'volume_size': 30,
                        }
                    },
                ],
            },
            'feature_flag_service': {
                'flags': {
                    'block_database_writes': False,
                }
            },
            'backend': {
                'cpu': 2048,
                'memory_limit_mib': 4096,
                'desired_count': 1,
                'max_capacity': 4,
                'ini_name': 'sandbox.ini',
                'use_postgres_named': 'Postgres',
                'read_from_opensearch_named': 'Opensearch27',
                'write_to_opensearch_named': 'Opensearch27',
            },
            'invalidation_service': {
                'cpu': 256,
                'memory_limit_mib': 512,
                'min_scaling_capacity': 1,
                'max_scaling_capacity': 2,
            },
            'indexing_service': {
                'cpu': 256,
                'memory_limit_mib': 512,
                'min_scaling_capacity': 1,
                'max_scaling_capacity': 4,
            },
            'tags': [
            ],
            'url_prefix': 'api',
        },
        'production': {
            'postgres': {
                'instances': [
                    {
                        'construct_id': 'Postgres',
                        'on': True,
                        'props': {
                            'allocated_storage': 10,
                            'max_allocated_storage': 20,
                            'instance_type': InstanceType.of(
                                InstanceClass.BURSTABLE3,
                                InstanceSize.MEDIUM,
                            ),
                        },
                    },
                ],
            },
            'opensearch': {
                'clusters': [
                    {
                        'construct_id': 'Opensearch27',
                        'on': True,
                        'props': {
                            'capacity': CapacityConfig(
                                data_node_instance_type='m6g.xlarge.search',
                                data_nodes=1,
                            ),
                            'engine_version': EngineVersion.OPENSEARCH_2_7,
                            'volume_size': 30,
                        }
                    },
                ],
            },
            'feature_flag_service': {
                'flags': {
                    'block_database_writes': False,
                }
            },
            'backend': {
                'cpu': 2048,
                'memory_limit_mib': 4096,
                'desired_count': 1,
                'max_capacity': 4,
                'ini_name': 'production.ini',
                'use_postgres_named': 'Postgres',
                'read_from_opensearch_named': 'Opensearch27',
                'write_to_opensearch_named': 'Opensearch27',
            },
            'invalidation_service': {
                'cpu': 256,
                'memory_limit_mib': 512,
                'min_scaling_capacity': 1,
                'max_scaling_capacity': 2,
            },
            'indexing_service': {
                'cpu': 256,
                'memory_limit_mib': 512,
                'min_scaling_capacity': 1,
                'max_scaling_capacity': 4,
            },
            'tags': [
            ],
            'url_prefix': 'api',
        },
    }
}


@dataclass
class Common:
    organization_name: str = 'igvf-dacc'
    project_name: str = 'igvfd'
    default_region: str = 'us-west-2'
    aws_cdk_version: str = '2.114.1'


@dataclass
class Config:
    name: str
    branch: str
    postgres: Dict[str, Any]
    opensearch: Dict[str, Any]
    feature_flag_service: Dict[str, Any]
    backend: Dict[str, Any]
    invalidation_service: Dict[str, Any]
    indexing_service: Dict[str, Any]
    tags: List[Tuple[str, str]]
    url_prefix: Optional[str] = None
    use_subdomain: bool = True
    common: Common = field(
        default_factory=Common
    )


@dataclass
class PipelineConfig:
    name: str
    branch: str
    pipeline: str
    existing_resources_class: ExistingResourcesClass
    account_and_region: Environment
    tags: List[Tuple[str, str]]
    cross_account_keys: bool = False
    common: Common = field(
        default_factory=Common
    )


def build_config_from_name(name: str, **kwargs: Any) -> Config:
    return Config(
        **{
            **config['environment'][name],
            **kwargs,
            **{'name': name},
        }
    )


def build_pipeline_config_from_name(name: str, **kwargs: Any) -> PipelineConfig:
    return PipelineConfig(
        **{
            **config['pipeline'][name],
            **kwargs,
            **{'name': name},
        }
    )


def get_config_name_from_branch(branch: str) -> str:
    if branch == 'dev':
        return 'dev'
    return 'demo'


def get_pipeline_config_name_from_branch(branch: str) -> str:
    if branch == 'dev':
        return 'dev'
    if branch == 'main':
        return 'production'
    return 'demo'
