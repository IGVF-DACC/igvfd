import pytest


def test_tags_add_environment_tag(config):
    from aws_cdk import App
    from aws_cdk import Stack
    from infrastructure.tags import add_environment_tag
    app = App()
    stack = Stack(
        app,
        'TestStack'
    )
    add_environment_tag(stack, config)
    cloud_assembly = app.synth()
    test_stack = cloud_assembly.get_stack_by_name(
        'TestStack'
    )
    assert test_stack.tags == {
        'environment': 'demo'
    }


def test_tags_add_project_tag(config):
    from aws_cdk import App
    from aws_cdk import Stack
    from infrastructure.tags import add_project_tag
    app = App()
    stack = Stack(
        app,
        'TestStack'
    )
    add_project_tag(stack, config)
    cloud_assembly = app.synth()
    test_stack = cloud_assembly.get_stack_by_name(
        'TestStack'
    )
    assert test_stack.tags == {
        'project': 'igvfd'
    }


def test_tags_add_branch_tag(config):
    from aws_cdk import App
    from aws_cdk import Stack
    from infrastructure.tags import add_branch_tag
    app = App()
    stack = Stack(
        app,
        'TestStack'
    )
    add_branch_tag(stack, config)
    cloud_assembly = app.synth()
    test_stack = cloud_assembly.get_stack_by_name(
        'TestStack'
    )
    assert test_stack.tags == {
        'branch': 'some-branch'
    }


def test_tags_add_config_tags(config):
    from aws_cdk import App
    from aws_cdk import Stack
    from infrastructure.tags import add_config_tags
    app = App()
    stack = Stack(
        app,
        'TestStack'
    )
    add_config_tags(stack, config)
    cloud_assembly = app.synth()
    test_stack = cloud_assembly.get_stack_by_name(
        'TestStack'
    )
    assert test_stack.tags == {
        'test': 'tag'
    }


def test_tags_add_tags_to_stack(config):
    from aws_cdk import App
    from aws_cdk import Stack
    from infrastructure.tags import add_tags_to_stack
    app = App()
    stack = Stack(
        app,
        'TestStack'
    )
    add_tags_to_stack(stack, config)
    cloud_assembly = app.synth()
    test_stack = cloud_assembly.get_stack_by_name(
        'TestStack'
    )
    assert test_stack.tags == {
        'environment': 'demo',
        'branch': 'some-branch',
        'project': 'igvfd',
        'test': 'tag'
    }


def test_tags_add_tags_to_stack_from_pipeline_config(pipeline_config):
    from aws_cdk import App
    from aws_cdk import Stack
    from infrastructure.tags import add_tags_to_stack
    app = App()
    stack = Stack(
        app,
        'TestStack'
    )
    add_tags_to_stack(stack, pipeline_config)
    cloud_assembly = app.synth()
    test_stack = cloud_assembly.get_stack_by_name(
        'TestStack'
    )
    assert test_stack.tags == {
        'environment': 'demo',
        'branch': 'some-branch',
        'project': 'igvfd',
        'test': 'tag'
    }
