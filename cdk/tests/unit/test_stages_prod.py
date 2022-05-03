import pytest


def test_stages_prod_initialize_prod_stage():
    from aws_cdk import Stage
    from aws_cdk import App
    from infrastructure.stages.prod import ProdDeployStage
    app = App()
    prod_deploy_stage = ProdDeployStage(
        app,
        'TestProdDeployStage'
    )
    assert isinstance(prod_deploy_stage, Stage)
