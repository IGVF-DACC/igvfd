import aws_cdk as core
import aws_cdk.assertions as assertions

from infrastructure.stacks.backend import BackendStack


def test_stacks_backend_backend_stack_created():
    app = core.App()
