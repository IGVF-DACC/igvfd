from dataclasses import dataclass

from typing import Optional


config = {
    'org_name': 'igvf-dacc',
    'project_name': 'igvfd',
    'default_branch': 'main',
    'region': 'us-west-2',
    'environment': {
        'demo': {
            'snapshot_source_db_identifier': 'ip197tomb39f7o0',
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


def build_config_from_name(name, **kwargs):
    return Config(
        **{
            **config['environment'][name],
            **kwargs,
        }
    )


def get_config_name_from_branch(branch: str):
    if branch == 'dev':
        return 'dev'
    return 'demo'
