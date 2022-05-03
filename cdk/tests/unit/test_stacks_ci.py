import pytest

from aws_cdk.assertions import Template


def test_stacks_ci_initialize_ci_stack():
    from aws_cdk import App
    from infrastructure.stacks.ci import ContinuousIntegrationStack
    from infrastructure.constructs.existing import igvf_dev
    app = App()
    ci = ContinuousIntegrationStack(
        app,
        'TestContinuousIntegrationStack',
        existing_resources_class=igvf_dev.Resources,
        env=igvf_dev.US_WEST_2,
    )
    template = Template.from_stack(ci)
    template.has_resource_properties(
        'AWS::CodeBuild::Project',
        {
            'BadgeEnabled': True,
            'Visibility': 'PUBLIC_READ',
        }
    )
    template.has_resource_properties(
        'AWS::IAM::Policy',
        {
            'PolicyDocument': {
                'Statement': [
                    {
                        'Action': 'logs:GetLogEvents',
                        'Effect': 'Allow',
                        'Resource': {
                            'Fn::Join': [
                                '',
                                [
                                    'arn:',
                                    {
                                        'Ref': 'AWS::Partition'
                                    },
                                    ':logs:us-west-2:109189702753:log-group:/aws/codebuild/',
                                    {
                                        'Ref': 'ContinuousIntegrationigvfdContinuousIntegration1CD8EFED'
                                    },
                                    ':*'
                                ]
                            ]
                        }
                    }
                ],
                'Version': '2012-10-17'
            },
            'PolicyName': 'ContinuousIntegrationResourceAccessRoleDefaultPolicyC7085190',
            'Roles': [
                {
                    'Ref': 'ContinuousIntegrationResourceAccessRole2093716E'
                }
            ]
        }
    )
