import pytest

from aws_cdk.assertions import Template


def test_constructs_ci_initialize_ci_construct(stack, mocker):
    from infrastructure.constructs.ci import ContinuousIntegration
    from aws_cdk.aws_secretsmanager import Secret
    docker_hub_credentials = mocker.Mock()
    docker_hub_credentials.secret = Secret(
        stack,
        'TestSecret',
    )
    ci = ContinuousIntegration(
        stack,
        'TestContinuousIntegration',
        github_owner='some-org',
        github_repo='some-repo',
        build_spec={},
        docker_hub_credentials=docker_hub_credentials,
    )
    template = Template.from_stack(stack)
    template.has_resource_properties(
        'AWS::CodeBuild::Project',
        {
            'Artifacts': {
                'Type': 'NO_ARTIFACTS'
            },
            'Environment': {
                'ComputeType': 'BUILD_GENERAL1_SMALL',
                'Image': 'aws/codebuild/standard:5.0',
                'ImagePullCredentialsType': 'CODEBUILD',
                'PrivilegedMode': True,
                'Type': 'LINUX_CONTAINER'
            },
            'ServiceRole': {
                'Fn::GetAtt': [
                    'TestContinuousIntegrationigvfdContinuousIntegrationRole1FA25164',
                    'Arn'
                ]
            },
            'Source': {
                'BuildSpec': '{}',
                'Location': 'https://github.com/some-org/some-repo.git',
                'ReportBuildStatus': True,
                'Type': 'GITHUB'
            },
            'BadgeEnabled': True,
            'Cache': {
                'Modes': [
                    'LOCAL_DOCKER_LAYER_CACHE'
                ],
                'Type': 'LOCAL'
            },
            'EncryptionKey': 'alias/aws/s3',
            'ResourceAccessRole': {
                'Fn::GetAtt': [
                    'TestContinuousIntegrationResourceAccessRole69FFBBDF',
                    'Arn'
                ]
            },
            'Triggers': {
                'Webhook': True
            },
            'Visibility': 'PUBLIC_READ'
        }
    )
    template.resource_count_is(
        'AWS::SecretsManager::Secret',
        1
    )
    template.resource_count_is(
        'AWS::IAM::Role',
        2
    )
    template.has_resource_properties(
        'AWS::IAM::Policy',
        {
            'PolicyDocument': {
                'Statement': [
                    {
                        'Action': [
                            'logs:CreateLogGroup',
                            'logs:CreateLogStream',
                            'logs:PutLogEvents'
                        ],
                        'Effect': 'Allow',
                        'Resource': [
                            {
                                'Fn::Join': [
                                    '',
                                    [
                                        'arn:',
                                        {
                                            'Ref': 'AWS::Partition'
                                        },
                                        ':logs:',
                                        {
                                            'Ref': 'AWS::Region'
                                        },
                                        ':',
                                        {
                                            'Ref': 'AWS::AccountId'
                                        },
                                        ':log-group:/aws/codebuild/',
                                        {
                                            'Ref': 'TestContinuousIntegrationigvfdContinuousIntegration42002874'
                                        }
                                    ]
                                ]
                            },
                            {
                                'Fn::Join': [
                                    '',
                                    [
                                        'arn:',
                                        {
                                            'Ref': 'AWS::Partition'
                                        },
                                        ':logs:',
                                        {
                                            'Ref': 'AWS::Region'
                                        },
                                        ':',
                                        {
                                            'Ref': 'AWS::AccountId'
                                        },
                                        ':log-group:/aws/codebuild/',
                                        {
                                            'Ref': 'TestContinuousIntegrationigvfdContinuousIntegration42002874'
                                        },
                                        ':*'
                                    ]
                                ]
                            }
                        ]
                    },
                    {
                        'Action': [
                            'codebuild:CreateReportGroup',
                            'codebuild:CreateReport',
                            'codebuild:UpdateReport',
                            'codebuild:BatchPutTestCases',
                            'codebuild:BatchPutCodeCoverages'
                        ],
                        'Effect': 'Allow',
                        'Resource': {
                            'Fn::Join': [
                                '',
                                [
                                    'arn:',
                                    {
                                        'Ref': 'AWS::Partition'
                                    },
                                    ':codebuild:',
                                    {
                                        'Ref': 'AWS::Region'
                                    },
                                    ':',
                                    {
                                        'Ref': 'AWS::AccountId'
                                    },
                                    ':report-group/',
                                    {
                                        'Ref': 'TestContinuousIntegrationigvfdContinuousIntegration42002874'
                                    },
                                    '-*'
                                ]
                            ]
                        }
                    },
                    {
                        'Action': [
                            'secretsmanager:GetSecretValue',
                            'secretsmanager:DescribeSecret'
                        ],
                        'Effect': 'Allow',
                        'Resource': {
                            'Ref': 'TestSecret16AF87B1'
                        }
                    }
                ],
                'Version': '2012-10-17'
            },
            'PolicyName': 'TestContinuousIntegrationigvfdContinuousIntegrationRoleDefaultPolicy79DDAAC5',
            'Roles': [
                {
                    'Ref': 'TestContinuousIntegrationigvfdContinuousIntegrationRole1FA25164'
                }
            ]
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
                                    ':logs:',
                                    {
                                        'Ref': 'AWS::Region'
                                    },
                                    ':',
                                    {
                                        'Ref': 'AWS::AccountId'
                                    },
                                    ':log-group:/aws/codebuild/',
                                    {
                                        'Ref': 'TestContinuousIntegrationigvfdContinuousIntegration42002874'
                                    },
                                    ':*'
                                ]
                            ]
                        }
                    }
                ],
                'Version': '2012-10-17'
            },
            'PolicyName': 'TestContinuousIntegrationResourceAccessRoleDefaultPolicy93697724',
            'Roles': [
                {
                    'Ref': 'TestContinuousIntegrationResourceAccessRole69FFBBDF'
                }
            ]
        }
    )
