import pytest

from aws_cdk.assertions import Template


def test_constructs_opensearch_initialize_opensearch_construct(stack, vpc, instance_type, mocker, config, existing_resources):
    from infrastructure.constructs.opensearch import Opensearch
    from infrastructure.constructs.opensearch import OpensearchProps
    opensearch = Opensearch(
        stack,
        'Opensearch',
        props=OpensearchProps(
            **config.opensearch,
            config=config,
            existing_resources=existing_resources
        )
    )
    template = Template.from_stack(stack)
    template.has_resource_properties(
        'AWS::OpenSearchService::Domain',
        {
            'AdvancedOptions': {
                'indices.query.bool.max_clause_count': '8096'
            },
            'ClusterConfig': {
                'DedicatedMasterEnabled': False,
                'InstanceCount': 1,
                'InstanceType': 't3.small.search',
                'ZoneAwarenessEnabled': False
            },
            'DomainEndpointOptions': {
                'EnforceHTTPS': False,
                'TLSSecurityPolicy': 'Policy-Min-TLS-1-0-2019-07'
            },
            'EBSOptions': {
                'EBSEnabled': True,
                'VolumeSize': 10,
                'VolumeType': 'gp2'
            },
            'EncryptionAtRestOptions': {
                'Enabled': False
            },
            'EngineVersion': 'OpenSearch_1.2',
            'LogPublishingOptions': {
                'ES_APPLICATION_LOGS': {
                    'CloudWatchLogsLogGroupArn': {
                        'Fn::GetAtt': [
                            'OpensearchDomainAppLogs191CCADD',
                            'Arn'
                        ]
                    },
                    'Enabled': True
                },
                'SEARCH_SLOW_LOGS': {
                    'CloudWatchLogsLogGroupArn': {
                        'Fn::GetAtt': [
                            'OpensearchDomainSlowSearchLogsCB6C5516',
                            'Arn'
                        ]
                    },
                    'Enabled': True
                },
                'INDEX_SLOW_LOGS': {
                    'CloudWatchLogsLogGroupArn': {
                        'Fn::GetAtt': [
                            'OpensearchDomainSlowIndexLogs76621B18',
                            'Arn'
                        ]
                    },
                    'Enabled': True
                }
            },
            'NodeToNodeEncryptionOptions': {
                'Enabled': False
            },
            'Tags': [
                {
                    'Key': 'branch',
                    'Value': 'some-branch'
                }
            ],
            'VPCOptions': {
                'SecurityGroupIds': [
                    {
                        'Fn::GetAtt': [
                            'OpensearchDomainSecurityGroup046A436D',
                            'GroupId'
                        ]
                    }
                ],
                'SubnetIds': []
            }
        }
    )
    template.resource_count_is(
        'Custom::OpenSearchAccessPolicy',
        1
    )
    template.resource_count_is(
        'AWS::CloudWatch::Alarm',
        6
    )
