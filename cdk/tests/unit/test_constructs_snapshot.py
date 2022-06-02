import pytest


from aws_cdk.assertions import Template


def test_constructs_snapshot_initialize_latest_snapshot_from_db(stack):
    from infrastructure.constructs.snapshot import LatestSnapshotFromDB
    latest_snapshot = LatestSnapshotFromDB(
        stack,
        'LatestSnapshotFromDB',
        db_instance_identifier='xyz123',
    )
    template = Template.from_stack(stack)
    template.has_resource_properties(
        'AWS::CloudFormation::CustomResource',
        {
            'ServiceToken': {
                'Fn::GetAtt': [
                    'LatestSnapshotFromDBProviderframeworkonEventF9445CCD',
                    'Arn'
                ]
            },
            'db_instance_identifier': 'xyz123'
        }
    )
    template.has_resource_properties(
        'AWS::Lambda::Function',
        {
            'Handler': 'main.custom_resource_handler',
            'Runtime': 'python3.9',
            'Timeout': 60
        }
    )
    template.has_resource_properties(
        'AWS::IAM::Policy',
        {
            'PolicyDocument': {
                'Statement': [
                    {
                        'Action': 'rds:DescribeDBSnapshots',
                        'Effect': 'Allow',
                        'Resource': '*'
                    }
                ],
                'Version': '2012-10-17'
            }
        }
    )
