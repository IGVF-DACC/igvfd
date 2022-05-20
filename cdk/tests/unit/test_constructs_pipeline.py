import pytest

from aws_cdk.assertions import Template


def test_constructs_pipeline_initialize_basic_self_updating_pipeline_construct(stack, secret, mocker, config):
    from infrastructure.constructs.pipeline import BasicSelfUpdatingPipeline
    from infrastructure.constructs.pipeline import BasicSelfUpdatingPipelineProps
    existing_resources = mocker.Mock()
    existing_resources.code_star_connection.arn = 'some-arn'
    existing_resources.docker_hub_credentials.secret = secret
    pipeline = BasicSelfUpdatingPipeline(
        stack,
        'TestBasicSelfUpdatingPipeline',
        props=BasicSelfUpdatingPipelineProps(
            github_repo='ABC/xyz',
            existing_resources=existing_resources,
            config=config,
        )
    )
    template = Template.from_stack(stack)
    template.has_resource_properties(
        'AWS::CodePipeline::Pipeline',
        {
            'RoleArn': {
                'Fn::GetAtt': [
                    'TestBasicSelfUpdatingPipelineCodePipelineRole19B5B1C6',
                    'Arn'
                ]
            },
            'Stages': [
                {
                    'Actions': [
                        {
                            'ActionTypeId': {
                                'Category': 'Source',
                                'Owner': 'AWS',
                                'Provider': 'CodeStarSourceConnection',
                                'Version': '1'
                            },
                            'Configuration': {
                                'ConnectionArn': 'some-arn',
                                'FullRepositoryId': 'ABC/xyz',
                                'BranchName': 'some-branch'
                            },
                            'Name': 'ABC_xyz',
                            'OutputArtifacts': [
                                {
                                    'Name': 'ABC_xyz_Source'
                                }
                            ],
                            'RoleArn': {
                                'Fn::GetAtt': [
                                    'TestBasicSelfUpdatingPipelineCodePipelineSourceABCxyzCodePipelineActionRole13A31726',
                                    'Arn'
                                ]
                            },
                            'RunOrder': 1
                        }
                    ],
                    'Name': 'Source'
                },
                {
                    'Actions': [
                        {
                            'ActionTypeId': {
                                'Category': 'Build',
                                'Owner': 'AWS',
                                'Provider': 'CodeBuild',
                                'Version': '1'
                            },
                            'Configuration': {
                                'ProjectName': {
                                    'Ref': 'TestBasicSelfUpdatingPipelineCodePipelineBuildSynthStepCdkBuildProjectC378F9B9'
                                },
                            },
                            'InputArtifacts': [
                                {
                                    'Name': 'ABC_xyz_Source'
                                }
                            ],
                            'Name': 'SynthStep',
                            'OutputArtifacts': [
                                {
                                    'Name': 'SynthStep_Output'
                                }
                            ],
                            'RoleArn': {
                                'Fn::GetAtt': [
                                    'TestBasicSelfUpdatingPipelineCodePipelineBuildSynthStepCodePipelineActionRole6ECE61D5',
                                    'Arn'
                                ]
                            },
                            'RunOrder': 1
                        }
                    ],
                    'Name': 'Build'
                },
                {
                    'Actions': [
                        {
                            'ActionTypeId': {
                                'Category': 'Build',
                                'Owner': 'AWS',
                                'Provider': 'CodeBuild',
                                'Version': '1'
                            },
                            'Configuration': {
                                'ProjectName': {
                                    'Ref': 'TestBasicSelfUpdatingPipelineCodePipelineUpdatePipelineSelfMutationCFEBBD4C'
                                },
                            },
                            'InputArtifacts': [
                                {
                                    'Name': 'SynthStep_Output'
                                }
                            ],
                            'Name': 'SelfMutate',
                            'RoleArn': {
                                'Fn::GetAtt': [
                                    'TestBasicSelfUpdatingPipelineCodePipelineUpdatePipelineSelfMutateCodePipelineActionRole7F53C12C',
                                    'Arn'
                                ]
                            },
                            'RunOrder': 1
                        }
                    ],
                    'Name': 'UpdatePipeline'
                }
            ],
            'ArtifactStore': {
                'Location': {
                    'Ref': 'TestBasicSelfUpdatingPipelineCodePipelineArtifactsBucket2E875062'
                },
                'Type': 'S3'
            },
            'RestartExecutionOnUpdate': True
        }
    )
    template.has_resource_properties(
        'AWS::CodeBuild::Project',
        {
            'Artifacts': {
                'Type': 'CODEPIPELINE'
            },
            'Environment': {
                'ComputeType': 'BUILD_GENERAL1_SMALL',
                'EnvironmentVariables': [
                    {
                        'Name': 'BRANCH',
                        'Type': 'PLAINTEXT',
                        'Value': 'some-branch'
                    }
                ],
                'Image': 'aws/codebuild/standard:5.0',
                'ImagePullCredentialsType': 'CODEBUILD',
                'PrivilegedMode': True,
                'Type': 'LINUX_CONTAINER'
            },
            'ServiceRole': {
                'Fn::GetAtt': [
                    'TestBasicSelfUpdatingPipelineCodePipelineBuildSynthStepCdkBuildProjectRole4C3CD640',
                    'Arn'
                ]
            },
            'Cache': {
                'Type': 'NO_CACHE'
            },
            'Description': 'Pipeline step Default/Pipeline/Build/SynthStep',
            'EncryptionKey': 'alias/aws/s3'
        }
    )
    template.has_resource_properties(
        'AWS::IAM::Policy',
        {
            'PolicyDocument': {
                'Statement': [
                    {
                        'Action': [
                            's3:GetObject*',
                            's3:GetBucket*',
                            's3:List*',
                            's3:DeleteObject*',
                            's3:PutObject',
                            's3:PutObjectLegalHold',
                            's3:PutObjectRetention',
                            's3:PutObjectTagging',
                            's3:PutObjectVersionTagging',
                            's3:Abort*'
                        ],
                        'Effect': 'Allow',
                        'Resource': [
                            {
                                'Fn::GetAtt': [
                                    'TestBasicSelfUpdatingPipelineCodePipelineArtifactsBucket2E875062',
                                    'Arn'
                                ]
                            },
                            {
                                'Fn::Join': [
                                    '',
                                    [
                                        {
                                            'Fn::GetAtt': [
                                                'TestBasicSelfUpdatingPipelineCodePipelineArtifactsBucket2E875062',
                                                'Arn'
                                            ]
                                        },
                                        '/*'
                                    ]
                                ]
                            }
                        ]
                    },
                    {
                        'Action': 'sts:AssumeRole',
                        'Effect': 'Allow',
                        'Resource': {
                            'Fn::GetAtt': [
                                'TestBasicSelfUpdatingPipelineCodePipelineSourceABCxyzCodePipelineActionRole13A31726',
                                'Arn'
                            ]
                        }
                    },
                    {
                        'Action': 'sts:AssumeRole',
                        'Effect': 'Allow',
                        'Resource': {
                            'Fn::GetAtt': [
                                'TestBasicSelfUpdatingPipelineCodePipelineBuildSynthStepCodePipelineActionRole6ECE61D5',
                                'Arn'
                            ]
                        }
                    },
                    {
                        'Action': 'sts:AssumeRole',
                        'Effect': 'Allow',
                        'Resource': {
                            'Fn::GetAtt': [
                                'TestBasicSelfUpdatingPipelineCodePipelineUpdatePipelineSelfMutateCodePipelineActionRole7F53C12C',
                                'Arn'
                            ]
                        }
                    }
                ],
                'Version': '2012-10-17'
            },
            'PolicyName': 'TestBasicSelfUpdatingPipelineCodePipelineRoleDefaultPolicy56CE15DF',
            'Roles': [
                {
                    'Ref': 'TestBasicSelfUpdatingPipelineCodePipelineRole19B5B1C6'
                }
            ]
        }
    )
    template.resource_count_is(
        'AWS::CodeBuild::Project',
        2
    )


def test_constructs_pipeline_initialize_continuous_deployment_pipeline_construct(mocker, config):
    from aws_cdk import Stack
    from aws_cdk import Environment
    from aws_cdk.aws_secretsmanager import Secret
    from aws_cdk.aws_chatbot import SlackChannelConfiguration
    from infrastructure.constructs.pipeline import ContinuousDeploymentPipeline
    from infrastructure.constructs.pipeline import ContinuousDeploymentPipelineProps
    from infrastructure.constructs.existing import igvf_dev
    stack = Stack(
        env=igvf_dev.US_WEST_2
    )
    existing_resources = mocker.Mock()
    existing_resources.code_star_connection.arn = 'some-arn'
    existing_resources.docker_hub_credentials.secret = Secret(
        stack,
        'TestSecret',
    )
    existing_resources.notification.encode_dcc_chatbot = SlackChannelConfiguration(
        stack,
        'TestChatbot',
        slack_channel_configuration_name='some-config-name',
        slack_channel_id='some-channel-id',
        slack_workspace_id='some-workspace-id',
    )
    pipeline = ContinuousDeploymentPipeline(
        stack,
        'TestContinuousDeploymentPipeline',
        props=ContinuousDeploymentPipelineProps(
            github_repo='ABC/xyz',
            existing_resources=existing_resources,
            config=config,
        )
    )
    template = Template.from_stack(stack)
    template.has_resource_properties(
        'AWS::CodePipeline::Pipeline',
        {
            'RoleArn': {
                'Fn::GetAtt': [
                    'TestContinuousDeploymentPipelineCodePipelineRole38D8F107',
                    'Arn'
                ]
            },
            'Stages': [
                {
                    'Actions': [
                        {
                            'ActionTypeId': {
                                'Category': 'Source',
                                'Owner': 'AWS',
                                'Provider': 'CodeStarSourceConnection',
                                'Version': '1'
                            },
                            'Configuration': {
                                'ConnectionArn': 'some-arn',
                                'FullRepositoryId': 'ABC/xyz',
                                'BranchName': 'some-branch'
                            },
                            'Name': 'ABC_xyz',
                            'OutputArtifacts': [
                                {
                                    'Name': 'ABC_xyz_Source'
                                }
                            ],
                            'RoleArn': {
                                'Fn::GetAtt': [
                                    'TestContinuousDeploymentPipelineCodePipelineSourceABCxyzCodePipelineActionRoleC92D665C',
                                    'Arn'
                                ]
                            },
                            'RunOrder': 1
                        }
                    ],
                    'Name': 'Source'
                },
                {
                    'Actions': [
                        {
                            'ActionTypeId': {
                                'Category': 'Build',
                                'Owner': 'AWS',
                                'Provider': 'CodeBuild',
                                'Version': '1'
                            },
                            'Configuration': {
                                'ProjectName': {
                                    'Ref': 'TestContinuousDeploymentPipelineCodePipelineBuildSynthStepCdkBuildProject31DA7614'
                                },
                            },
                            'InputArtifacts': [
                                {
                                    'Name': 'ABC_xyz_Source'
                                }
                            ],
                            'Name': 'SynthStep',
                            'OutputArtifacts': [
                                {
                                    'Name': 'SynthStep_Output'
                                }
                            ],
                            'RoleArn': {
                                'Fn::GetAtt': [
                                    'TestContinuousDeploymentPipelineCodePipelineBuildSynthStepCodePipelineActionRole7C5EF630',
                                    'Arn'
                                ]
                            },
                            'RunOrder': 1
                        }
                    ],
                    'Name': 'Build'
                },
                {
                    'Actions': [
                        {
                            'ActionTypeId': {
                                'Category': 'Build',
                                'Owner': 'AWS',
                                'Provider': 'CodeBuild',
                                'Version': '1'
                            },
                            'Configuration': {
                                'ProjectName': {
                                    'Ref': 'TestContinuousDeploymentPipelineCodePipelineUpdatePipelineSelfMutation9A9B071E'
                                },
                            },
                            'InputArtifacts': [
                                {
                                    'Name': 'SynthStep_Output'
                                }
                            ],
                            'Name': 'SelfMutate',
                            'RoleArn': {
                                'Fn::GetAtt': [
                                    'TestContinuousDeploymentPipelineCodePipelineUpdatePipelineSelfMutateCodePipelineActionRole535C23EA',
                                    'Arn'
                                ]
                            },
                            'RunOrder': 1
                        }
                    ],
                    'Name': 'UpdatePipeline'
                },
                {
                    'Actions': [
                        {
                            'ActionTypeId': {
                                'Category': 'Build',
                                'Owner': 'AWS',
                                'Provider': 'CodeBuild',
                                'Version': '1'
                            },
                            'Configuration': {
                                'ProjectName': {
                                    'Ref': 'TestContinuousDeploymentPipelineCodePipelineAssetsDockerAsset1AD9A7B99'
                                }
                            },
                            'InputArtifacts': [
                                {
                                    'Name': 'SynthStep_Output'
                                }
                            ],
                            'Name': 'DockerAsset1',
                            'RoleArn': {
                                'Fn::GetAtt': [
                                    'TestContinuousDeploymentPipelineCodePipelineAssetsDockerAsset1CodePipelineActionRole21603C3A',
                                    'Arn'
                                ]
                            },
                            'RunOrder': 1
                        },
                        {
                            'ActionTypeId': {
                                'Category': 'Build',
                                'Owner': 'AWS',
                                'Provider': 'CodeBuild',
                                'Version': '1'
                            },
                            'Configuration': {
                                'ProjectName': {
                                    'Ref': 'TestContinuousDeploymentPipelineCodePipelineAssetsDockerAsset2BA745669'
                                }
                            },
                            'InputArtifacts': [
                                {
                                    'Name': 'SynthStep_Output'
                                }
                            ],
                            'Name': 'DockerAsset2',
                            'RoleArn': {
                                'Fn::GetAtt': [
                                    'TestContinuousDeploymentPipelineCodePipelineAssetsDockerAsset2CodePipelineActionRoleC8856490',
                                    'Arn'
                                ]
                            },
                            'RunOrder': 1
                        }
                    ],
                    'Name': 'Assets'
                },
                {
                    'Actions': [
                        {
                            'ActionTypeId': {
                                'Category': 'Deploy',
                                'Owner': 'AWS',
                                'Provider': 'CloudFormation',
                                'Version': '1'
                            },
                            'Configuration': {
                                'StackName': 'igvfd-some-branch-DeployContinuousIntegration-ContinuousIntegrationStack',
                                'Capabilities': 'CAPABILITY_NAMED_IAM,CAPABILITY_AUTO_EXPAND',
                                'RoleArn': {
                                    'Fn::Join': [
                                        '',
                                        [
                                            'arn:',
                                            {
                                                'Ref': 'AWS::Partition'
                                            },
                                            ':iam::109189702753:role/cdk-hnb659fds-cfn-exec-role-109189702753-us-west-2'
                                        ]
                                    ]
                                },
                                'ActionMode': 'CHANGE_SET_REPLACE',
                                'ChangeSetName': 'PipelineChange',
                                'TemplatePath': 'SynthStep_Output::assembly-Default-TestContinuousDeploymentPipeline-igvfd-some-branch-DeployContinuousIntegration/TestContinuousDeploymentPipelineigvfdsomebranchDeployContinuousIntegrationContinuousIntegrationStack969A0C2E.template.json'
                            },
                            'InputArtifacts': [
                                {
                                    'Name': 'SynthStep_Output'
                                }
                            ],
                            'Name': 'Prepare',
                            'RoleArn': {
                                'Fn::Join': [
                                    '',
                                    [
                                        'arn:',
                                        {
                                            'Ref': 'AWS::Partition'
                                        },
                                        ':iam::109189702753:role/cdk-hnb659fds-deploy-role-109189702753-us-west-2'
                                    ]
                                ]
                            },
                            'RunOrder': 1
                        },
                        {
                            'ActionTypeId': {
                                'Category': 'Deploy',
                                'Owner': 'AWS',
                                'Provider': 'CloudFormation',
                                'Version': '1'
                            },
                            'Configuration': {
                                'StackName': 'igvfd-some-branch-DeployContinuousIntegration-ContinuousIntegrationStack',
                                'ActionMode': 'CHANGE_SET_EXECUTE',
                                'ChangeSetName': 'PipelineChange'
                            },
                            'Name': 'Deploy',
                            'RoleArn': {
                                'Fn::Join': [
                                    '',
                                    [
                                        'arn:',
                                        {
                                            'Ref': 'AWS::Partition'
                                        },
                                        ':iam::109189702753:role/cdk-hnb659fds-deploy-role-109189702753-us-west-2'
                                    ]
                                ]
                            },
                            'RunOrder': 2
                        }
                    ],
                    'Name': 'igvfd-some-branch-DeployContinuousIntegration'
                },
                {
                    'Actions': [
                        {
                            'ActionTypeId': {
                                'Category': 'Deploy',
                                'Owner': 'AWS',
                                'Provider': 'CloudFormation',
                                'Version': '1'
                            },
                            'Configuration': {
                                'StackName': 'igvfd-some-branch-DeployDevelopment-PostgresStack',
                                'Capabilities': 'CAPABILITY_NAMED_IAM,CAPABILITY_AUTO_EXPAND',
                                'RoleArn': {
                                    'Fn::Join': [
                                        '',
                                        [
                                            'arn:',
                                            {
                                                'Ref': 'AWS::Partition'
                                            },
                                            ':iam::109189702753:role/cdk-hnb659fds-cfn-exec-role-109189702753-us-west-2'
                                        ]
                                    ]
                                },
                                'ActionMode': 'CHANGE_SET_REPLACE',
                                'ChangeSetName': 'PipelineChange',
                                'TemplatePath': 'SynthStep_Output::assembly-Default-TestContinuousDeploymentPipeline-igvfd-some-branch-DeployDevelopment/TestContinuousDeploymentPipelineigvfdsomebranchDeployDevelopmentPostgresStack0D31998D.template.json'
                            },
                            'InputArtifacts': [
                                {
                                    'Name': 'SynthStep_Output'
                                }
                            ],
                            'Name': 'PostgresStack.Prepare',
                            'RoleArn': {
                                'Fn::Join': [
                                    '',
                                    [
                                        'arn:',
                                        {
                                            'Ref': 'AWS::Partition'
                                        },
                                        ':iam::109189702753:role/cdk-hnb659fds-deploy-role-109189702753-us-west-2'
                                    ]
                                ]
                            },
                            'RunOrder': 1
                        },
                        {
                            'ActionTypeId': {
                                'Category': 'Deploy',
                                'Owner': 'AWS',
                                'Provider': 'CloudFormation',
                                'Version': '1'
                            },
                            'Configuration': {
                                'StackName': 'igvfd-some-branch-DeployDevelopment-PostgresStack',
                                'ActionMode': 'CHANGE_SET_EXECUTE',
                                'ChangeSetName': 'PipelineChange'
                            },
                            'Name': 'PostgresStack.Deploy',
                            'RoleArn': {
                                'Fn::Join': [
                                    '',
                                    [
                                        'arn:',
                                        {
                                            'Ref': 'AWS::Partition'
                                        },
                                        ':iam::109189702753:role/cdk-hnb659fds-deploy-role-109189702753-us-west-2'
                                    ]
                                ]
                            },
                            'RunOrder': 2
                        },
                        {
                            'ActionTypeId': {
                                'Category': 'Deploy',
                                'Owner': 'AWS',
                                'Provider': 'CloudFormation',
                                'Version': '1'
                            },
                            'Configuration': {
                                'StackName': 'igvfd-some-branch-DeployDevelopment-BackendStack',
                                'Capabilities': 'CAPABILITY_NAMED_IAM,CAPABILITY_AUTO_EXPAND',
                                'RoleArn': {
                                    'Fn::Join': [
                                        '',
                                        [
                                            'arn:',
                                            {
                                                'Ref': 'AWS::Partition'
                                            },
                                            ':iam::109189702753:role/cdk-hnb659fds-cfn-exec-role-109189702753-us-west-2'
                                        ]
                                    ]
                                },
                                'ActionMode': 'CHANGE_SET_REPLACE',
                                'ChangeSetName': 'PipelineChange',
                                'TemplatePath': 'SynthStep_Output::assembly-Default-TestContinuousDeploymentPipeline-igvfd-some-branch-DeployDevelopment/TestContinuousDeploymentPipelineigvfdsomebranchDeployDevelopmentBackendStackCEA09DF5.template.json'
                            },
                            'InputArtifacts': [
                                {
                                    'Name': 'SynthStep_Output'
                                }
                            ],
                            'Name': 'BackendStack.Prepare',
                            'RoleArn': {
                                'Fn::Join': [
                                    '',
                                    [
                                        'arn:',
                                        {
                                            'Ref': 'AWS::Partition'
                                        },
                                        ':iam::109189702753:role/cdk-hnb659fds-deploy-role-109189702753-us-west-2'
                                    ]
                                ]
                            },
                            'RunOrder': 3
                        },
                        {
                            'ActionTypeId': {
                                'Category': 'Deploy',
                                'Owner': 'AWS',
                                'Provider': 'CloudFormation',
                                'Version': '1'
                            },
                            'Configuration': {
                                'StackName': 'igvfd-some-branch-DeployDevelopment-BackendStack',
                                'ActionMode': 'CHANGE_SET_EXECUTE',
                                'ChangeSetName': 'PipelineChange'
                            },
                            'Name': 'BackendStack.Deploy',
                            'RoleArn': {
                                'Fn::Join': [
                                    '',
                                    [
                                        'arn:',
                                        {
                                            'Ref': 'AWS::Partition'
                                        },
                                        ':iam::109189702753:role/cdk-hnb659fds-deploy-role-109189702753-us-west-2'
                                    ]
                                ]
                            },
                            'RunOrder': 4
                        }
                    ],
                    'Name': 'igvfd-some-branch-DeployDevelopment'
                }
            ],
            'ArtifactStore': {
                'Location': {
                    'Ref': 'TestContinuousDeploymentPipelineCodePipelineArtifactsBucket3F64CEC7'
                },
                'Type': 'S3'
            }
        }
    )
    template.resource_count_is(
        'AWS::S3::Bucket',
        1
    )
    template.resource_count_is(
        'AWS::Chatbot::SlackChannelConfiguration',
        1
    )
