import boto3

import logging


logging.basicConfig(
    level=logging.INFO,
    force=True
)


def get_appconfig_client():
    return boto3.client('appconfig')


def get_all_version_nubmers(client, application_id, configuration_profile_id):
    return [
        x['VersionNumber']
        for x in client.list_hosted_configuration_versions(
            ApplicationId=application_id,
            ConfigurationProfileId=configuration_profile_id,
            MaxResults=50
        )['Items']
    ]


def delete_all_versions(client, application_id, configuration_profile_id, version_numbers):
    for version_number in version_numbers:
        try:
            response = client.delete_hosted_configuration_version(
                ApplicationId=application_id,
                ConfigurationProfileId=configuration_profile_id,
                VersionNumber=version_number
            )
            logging.info(f'Deleting version {version_number}: {response}')
        except Exception as e:
            logging.exception(f'Delete exception for version {version_number}')


def delete_all_hosted_configuration_versions(event, context):
    application_id = event['ResourceProperties']['application_id']
    configuration_profile_id = event['ResourceProperties']['configuration_profile_id']
    client = get_appconfig_client()
    version_numbers = get_all_version_nubmers(
        client,
        application_id,
        configuration_profile_id
    )
    delete_all_versions(
        client,
        application_id,
        configuration_profile_id,
        version_numbers
    )


def on_delete(event, context):
    delete_all_hosted_configuration_versions(event, context)


def custom_resource_handler(event, context):
    logging.warning(f'Event: {event}')
    if event['RequestType'] == 'Delete':
        return on_delete(event, context)
