import pytest


from aws_cdk.assertions import Template


def test_constructs_flag_initialize_feature_flag_service(stack, config):
    from infrastructure.constructs.flag import FeatureFlagServiceProps
    from infrastructure.constructs.flag import FeatureFlagService
    FeatureFlagService(
        stack,
        'FeatureFlagService',
        props=FeatureFlagServiceProps(
            flags={
                'some-flag': True,
                'some-other-flag': 'False',
                'another-flag': True,
            },
            config=config,
        )
    )
    template = Template.from_stack(stack)
    template.has_resource_properties(
        'AWS::AppConfig::Application',
        {
            'Name': 'igvfd-some-branch'
        }
    )
    template.has_resource_properties(
        'AWS::AppConfig::Environment',
        {
            'ApplicationId': {
                'Ref': 'FeatureFlagServiceApplicationB66919AF'
            },
            'Name': 'demo'
        }
    )
    template.has_resource_properties(
        'AWS::AppConfig::ConfigurationProfile',
        {
            'ApplicationId': {
                'Ref': 'FeatureFlagServiceApplicationB66919AF'
            },
            'LocationUri': 'hosted',
            'Name': 'igvfd-some-branch-demo-feature-flags',
            'Type': 'AWS.AppConfig.FeatureFlags'
        }
    )
    template.has_resource_properties(
        'AWS::AppConfig::DeploymentStrategy',
        {
            'DeploymentDurationInMinutes': 0,
            'GrowthFactor': 100,
            'Name': 'igvfd-some-branch-demo-deployment-strategy',
            'ReplicateTo': 'NONE'
        }
    )
    template.has_resource_properties(
        'AWS::AppConfig::HostedConfigurationVersion',
        {
            'ApplicationId': {
                'Ref': 'FeatureFlagServiceApplicationB66919AF'
            },
            'ConfigurationProfileId': {
                'Ref': 'FeatureFlagServiceConfigurationProfileB5E66ECD'
            },
            'Content': "{\"version\": \"1\", \"flags\": {\"some-flag\": {\"name\": \"some-flag\"}, \"some-other-flag\": {\"name\": \"some-other-flag\"}, \"another-flag\": {\"name\": \"another-flag\"}}, \"values\": {\"some-flag\": {\"enabled\": true}, \"some-other-flag\": {\"enabled\": \"False\"}, \"another-flag\": {\"enabled\": true}}}",
            'ContentType': 'application/json'
        }
    )
    template.has_resource_properties(
        'AWS::AppConfig::Deployment',
        {
            'ApplicationId': {
                'Ref': 'FeatureFlagServiceApplicationB66919AF'
            },
            'ConfigurationProfileId': {
                'Ref': 'FeatureFlagServiceConfigurationProfileB5E66ECD'
            },
            'ConfigurationVersion': {
                'Ref': 'FeatureFlagServiceHostedConfigurationVersionFCAE810E'
            },
            'DeploymentStrategyId': {
                'Ref': 'FeatureFlagServiceDeploymentStrategy65AA48C1'
            },
            'EnvironmentId': {
                'Ref': 'FeatureFlagServiceEnvironmentAA5FC5C3'
            }
        }
    )
    template.has_resource_properties(
        'AWS::IAM::Policy',
        {
            'PolicyDocument': {
                'Statement': [
                    {
                        'Action': [
                            'appconfig:ListHostedConfigurationVersions',
                            'appconfig:DeleteHostedConfigurationVersion'
                        ],
                        'Effect': 'Allow',
                        'Resource': '*'
                    }
                ]
            }
        }
    )
    template.resource_count_is(
        'AWS::CloudFormation::CustomResource',
        1
    )
