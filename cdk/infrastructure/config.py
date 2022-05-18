from dataclasses import dataclass

from typing import Any
from typing import Dict
from typing import Optional

from infrastructure.constants import DEV_DATABASE_IDENTIFIER


config: Dict[str, Any] = {
    'org_name': 'igvf-dacc',
    'project_name': 'igvfd',
    'default_branch': 'main',
    'region': 'us-west-2',
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
class Config:
    branch: str
    pipeline: str
    snapshot_source_db_identifier: Optional[str] = None


def build_config_from_name(name: str, **kwargs: Any) -> Config:
    return Config(
        **{
            **config['environment'][name],
            **kwargs,
        }
    )


def get_config_name_from_branch(branch: str) -> str:
    if branch == 'dev':
        return 'dev'
    return 'demo'
