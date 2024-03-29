import boto3
import json

import logging


logging.basicConfig(
    level=logging.INFO,
    force=True
)


def log(message):
    def decorator(func):
        def wrapper(*args, **kwargs):
            logging.info(f'MESSAGE from {func.__name__}: {message}')
            result = func(*args, **kwargs)
            logging.info(f'RESULT: {result}')
            return result
        return wrapper
    return decorator


def get_rds_client():
    return boto3.client('rds')


def get_describe_db_snapshots_paginator(client):
    return client.get_paginator('describe_db_snapshots')


def make_query(paginator, **kwargs):
    return paginator.paginate(**kwargs)


def get_results(query):
    for result in query:
        for snapshot in result['DBSnapshots']:
            yield snapshot


def sort_results_by_create_time(results):
    return sorted(
        results,
        key=lambda result: result['SnapshotCreateTime'],
        reverse=True
    )


def filter_results_by_db_instance_identifier(results, db_instance_identifier):
    filtered_results = [result for result in results if result['DBInstanceIdentifier'] == db_instance_identifier]
    return filtered_results


@log(message='Getting latest result')
def get_latest_result(sorted_results):
    return list(sorted_results)[0]


def get_latest_rds_snapshot_id(event, context):
    db_instance_identifier = event['ResourceProperties']['db_instance_identifier']
    client = get_rds_client()
    paginator = get_describe_db_snapshots_paginator(client)
    query = make_query(
        paginator,
        IncludeShared=True,
    )
    results = get_results(query)
    filtered_results = filter_results_by_db_instance_identifier(results, db_instance_identifier)
    sorted_results = sort_results_by_create_time(
        filtered_results
    )
    latest_result = get_latest_result(sorted_results)
    # Serialize datetime objects to str.
    return json.loads(
        json.dumps(
            latest_result,
            default=str,
        )
    )


def on_create(event, context):
    data = get_latest_rds_snapshot_id(event, context)
    return {
        'Data': data
    }


def custom_resource_handler(event, context):
    logging.warning(f'Event: {event}')
    if event['RequestType'] != 'Delete':
        return on_create(event, context)
