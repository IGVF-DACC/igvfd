import pytest


def test_stages_production_initialize_production_stages(config):
    from aws_cdk import App
    from infrastructure.stages.production import ProductionDeployStage
    app = App()
    production_deploy_stage = ProductionDeployStage(
        app,
        'TestProductionDeployStage',
        config=config,
    )
    cloud_assembly = production_deploy_stage.synth()
    assert [
        stack.stack_name
        for stack in cloud_assembly.stacks
    ] == [
        'TestProductionDeployStage-OpensearchStack',
        'TestProductionDeployStage-PostgresStack',
        'TestProductionDeployStage-BackendStack'
    ]
    for stack in cloud_assembly.stacks:
        assert stack.tags
