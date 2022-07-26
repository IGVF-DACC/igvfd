from dataclasses import dataclass

from typing import Any
from typing import Dict
from typing import Optional

from infrastructure.constants import DEV_DATABASE_IDENTIFIER


config: Dict[str, Any] = {
    'environment': {
        'demo': {
            'snapshot_source_db_identifier': DEV_DATABASE_IDENTIFIER,
            'pipeline': 'DemoDeploymentPipelineStack',
        },
        'dev': {
            'pipeline': 'ContinuousDeploymentPipelineStack',
        },
        'test': {},
        'prod': {}
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
    snapshot_arn: Optional[str] = None
    snapshot_source_db_identifier: Optional[str] = None
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
