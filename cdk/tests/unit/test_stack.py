import aws_cdk as core
import aws_cdk.assertions as assertions

from infrastructure.stack import BackendStack


def test_stack_backend_stack_created():
    app = core.App()
    stack = BackendStack(app, "cdk")
    template = assertions.Template.from_stack(stack)
    print(template)
    assert False
#    template.has_resource_properties("AWS::SQ::Queue", {
#         "VisibilityTimeout": 300
#     })
