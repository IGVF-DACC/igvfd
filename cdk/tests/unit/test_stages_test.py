import pytest


def test_stages_test_initialize_test_stage():
    from aws_cdk import Stage
    from aws_cdk import App
    from infrastructure.stages.test import TestDeployStage
    app = App()
    test_deploy_stage = TestDeployStage(
        app,
        'TestTestDeployStage'
    )
    assert isinstance(test_deploy_stage, Stage)
