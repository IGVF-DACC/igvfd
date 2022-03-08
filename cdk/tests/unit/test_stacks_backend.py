import aws_cdk as core
import aws_cdk.assertions as assertions

from infrastructure.stacks.backend import BackendStack


def test_stacks_backend_backend_stack_created():
    app = core.App()
    stack = BackendStack(
        app,
        'BackendStack',
    )
    template = assertions.Template.from_stack(stack)
    print(template.to_json())
    assert True
#    template.has_resource_properties("AWS::SQ::Queue", {
#         "VisibilityTimeout": 300
#     })
