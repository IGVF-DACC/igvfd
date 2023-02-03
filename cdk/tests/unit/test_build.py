import pytest

from aws_cdk.assertions import Template


def test_get_args_too_long_branch_name_raises_ValueError():
    from aws_cdk import App
    from infrastructure.build import Args
    from infrastructure.build import get_args
    app = App(
        context={
            'branch': 'seriously-this-branch-name-is-like-some-novel'
        }
    )
    with pytest.raises(ValueError) as e:
        args = get_args(app)
    assert str(e.value) == 'Branch length 45 exceeds the maximum branch length of 44 characters.'


def test_synth_get_args():
    from aws_cdk import App
    from infrastructure.build import Args
    from infrastructure.build import get_args
    app = App()
    with pytest.raises(ValueError) as e:
        args = get_args(app)
    assert str(e.value) == 'Must specify branch context: `-c branch=$BRANCH`'
    app = App(
        context={
            'branch': 'my-branch'
        }
    )
    args = get_args(app)
    assert isinstance(args, Args)
    assert args.branch == 'my-branch'
    assert args.config_name == 'demo'
    app = App(
        context={
            'branch': 'my-branch',
            'config-name': 'dev',
        }
    )
    args = get_args(app)
    assert isinstance(args, Args)
    assert args.branch == 'my-branch'
    assert args.config_name == 'dev'
    app = App(
        context={
            'branch': 'dev',
        }
    )
    args = get_args(app)
    assert isinstance(args, Args)
    assert args.branch == 'dev'
    assert args.config_name == 'dev'


def test_synth_get_config():
    from aws_cdk import App
    from infrastructure.build import get_args
    from infrastructure.build import get_config
    app = App(
        context={
            'branch': 'my-branch'
        }
    )
    args = get_args(app)
    config = get_config(args)
    assert config.branch == 'my-branch'
    assert config.pipeline == 'DemoDeploymentPipelineStack'
    assert config.account_and_region
    assert config.existing_resources_class
    assert config.common.project_name == 'igvfd'
    app = App(
        context={
            'branch': 'dev'
        }
    )
    args = get_args(app)
    config = get_config(args)
    assert config.branch == 'dev'
    assert config.pipeline == 'ContinuousDeploymentPipelineStack'
    assert config.common.project_name == 'igvfd'


def test_synth_add_deploy_pipeline_stack_to_app():
    from aws_cdk import App
    from infrastructure.build import get_args
    from infrastructure.build import get_config
    from infrastructure.build import add_deploy_pipeline_stack_to_app
    app = App()
    app = App(
        context={
            'branch': 'my-branch'
        }
    )
    args = get_args(app)
    config = get_config(args)
    add_deploy_pipeline_stack_to_app(app, config)
    child_paths = [
        child.node.path
        for child in app.node.children
    ]
    assert 'igvfd-my-branch-DemoDeploymentPipelineStack' in child_paths
    app = App()
    app = App(
        context={
            'branch': 'dev'
        }
    )
    args = get_args(app)
    config = get_config(args)
    add_deploy_pipeline_stack_to_app(app, config)
    child_paths = [
        child.node.path
        for child in app.node.children
    ]
    assert 'igvfd-dev-ContinuousDeploymentPipelineStack' in child_paths
    stack = app.node.find_child(
        'igvfd-dev-ContinuousDeploymentPipelineStack'
    )
    template = Template.from_stack(stack)
    template.has_resource_properties(
        'AWS::CodePipeline::Pipeline',
        {
            'Tags': [
                {
                    'Key': 'branch',
                    'Value': 'dev'
                },
                {
                    'Key': 'environment',
                    'Value': 'dev'
                },
                {
                    'Key': 'project',
                    'Value': 'igvfd'
                }
            ]
        }
    )


def test_synth_build():
    from aws_cdk import App
    from infrastructure.build import build
    app = App()
    app = App(
        context={
            'branch': 'my-branch'
        }
    )
    build(app)
    child_paths = [
        child.node.path
        for child in app.node.children
    ]
    assert 'igvfd-my-branch-DemoDeploymentPipelineStack' in child_paths
