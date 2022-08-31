from aws_cdk.aws_ec2 import InstanceType
from aws_cdk.aws_ec2 import InstanceClass
from aws_cdk.aws_ec2 import InstanceSize

from dataclasses import dataclass

from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from infrastructure.constants import DEV_DATABASE_IDENTIFIER


config: Dict[str, Any] = {
    'environment': {
        'demo': {
            'pipeline': 'DemoDeploymentPipelineStack',
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
            'backend': {
                'cpu': 1024,
                'memory_limit_mib': 2048,
                'desired_count': 1,
                'max_capacity': 4,
                'use_postgres_named': 'Postgres',
            },
            'tags': [
                ('time-to-live-hours', '-1'),
            ],
        },
        'dev': {
            'pipeline': 'ContinuousDeploymentPipelineStack',
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
            'backend': {
                'cpu': 1024,
                'memory_limit_mib': 2048,
                'desired_count': 1,
                'max_capacity': 4,
                'use_postgres_named': 'Postgres'
            },
            'tags': [
            ]
        },
        'test': {},
        'prod': {},
    }
}


@dataclass
class Common:
    organization_name: str = 'igvf-dacc'
    project_name: str = 'igvfd'
    default_region: str = 'us-west-2'
    aws_cdk_version: str = '2.21.0'


@dataclass
class Config:
    name: str
    branch: str
    pipeline: str
    postgres: Dict[str, Any]
    backend: Dict[str, Any]
    tags: List[Tuple[str, str]]
    common: Common = Common()


def build_config_from_name(name: str, **kwargs: Any) -> Config:
    return Config(
        **{
            **config['environment'][name],
            **kwargs,
            **{'name': name},
        }
    )


def get_config_name_from_branch(branch: str) -> str:
    if branch == 'dev':
        return 'dev'
    return 'demo'
