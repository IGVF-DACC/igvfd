import aws_cdk as cdk


class ProdDeployStage(cdk.Stage):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id,  **kwargs)
