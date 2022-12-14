import pytest


def test_stages_staging_initialize_staging_stages(config):
    from aws_cdk import App
    from infrastructure.stages.staging import StagingDeployStage
    app = App()
    staging_deploy_stage = StagingDeployStage(
        app,
        'TestStagingDeployStage',
        config=config,
    )
    cloud_assembly = staging_deploy_stage.synth()
    assert [
        stack.stack_name
        for stack in cloud_assembly.stacks
    ] == [
        'TestStagingDeployStage-OpensearchStack',
        'TestStagingDeployStage-PostgresStack',
        'TestStagingDeployStage-BackendStack'
    ]
    for stack in cloud_assembly.stacks:
        assert stack.tags
