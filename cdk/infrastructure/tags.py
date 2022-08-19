from aws_cdk import Stack
from aws_cdk import Tags

from infrastructure.config import Config


def add_environment_tag(stack: Stack, config: Config) -> None:
    Tags.of(stack).add(
        'environment',
        config.name
    )


def add_project_tag(stack: Stack, config: Config) -> None:
    Tags.of(stack).add(
        'project',
        config.common.project_name
    )


def add_branch_tag(stack: Stack, config: Config) -> None:
    Tags.of(stack).add(
        'branch',
        config.branch
    )


def add_config_tags(stack: Stack, config: Config) -> None:
    for (key, value) in config.tags:
        Tags.of(stack).add(key, value)


def add_tags_to_stack(stack: Stack, config: Config) -> None:
    add_project_tag(stack, config)
    add_branch_tag(stack, config)
    add_config_tags(stack, config)
