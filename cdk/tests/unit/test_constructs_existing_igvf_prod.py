import pytest


def test_constructs_existing_initialize_igvf_prod_construct():
    from aws_cdk import Stack
    from aws_cdk import Environment
    from infrastructure.constructs.existing.igvf_prod import Resources
    from shared_infrastructure.igvf_prod.domain import Domain
    from shared_infrastructure.igvf_prod.secret import DockerHubCredentials
    from shared_infrastructure.igvf_prod.secret import PortalCredentials
    from shared_infrastructure.igvf_prod.network import Network
    stack = Stack(
        env=Environment(
            region='us-east-1',
            account='123456789012'
        )
    )
    resources = Resources(
        stack,
        'TestExistingResources',
    )
    assert isinstance(resources.network, Network)
    assert isinstance(resources.network.vpc.vpc_id, str)
    assert isinstance(resources.domain, Domain)
    assert isinstance(resources.domain.name, str)
    assert isinstance(resources.domain.zone.hosted_zone_id, str)
    assert isinstance(resources.domain.certificate.certificate_arn, str)
    assert isinstance(resources.docker_hub_credentials, DockerHubCredentials)
    assert isinstance(resources.docker_hub_credentials.secret.secret_arn, str)
    assert isinstance(resources.portal_credentials, PortalCredentials)
    assert isinstance(resources.portal_credentials.indexing_service_key.secret_arn, str)
    assert isinstance(resources.code_star_connection.arn, str)
    assert isinstance(resources.notification.encode_dcc_chatbot.slack_channel_configuration_arn, str)
    assert isinstance(resources.bus.default.event_bus_arn, str)
    assert isinstance(resources.bucket_access_policies.download_igvf_files_policy.managed_policy_arn, str)
    assert isinstance(resources.bucket_access_policies.upload_igvf_files_policy.managed_policy_arn, str)
