import logging

import os

import sys

from subprocess import run
from subprocess import PIPE
from subprocess import STDOUT
from subprocess import CalledProcessError

from igvfd.events.remote.bus import InMemoryEventBus
from igvfd.events.remote.bus import EventBridgeEventBus

from igvfd.events.domain.batchupgrade import BatchUpgradeStarted
from igvfd.events.domain.batchupgrade import BatchUpgradeCompleted
from igvfd.events.domain.batchupgrade import BatchUpgradeFailed

from dataclasses import dataclass

from typing import Union


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BATCH_UPGRADE_COMMAND = [
    'batchupgrade',
]


@dataclass
class BatchUpgradeNotificationProps:
    bus: Union[InMemoryEventBus, EventBridgeEventBus]
    source: str


def get_bus():
    DEFAULT_EVENT_BUS = os.environ.get('DEFAULT_EVENT_BUS')
    if DEFAULT_EVENT_BUS is not None:
        return EventBridgeEventBus(
            name=DEFAULT_EVENT_BUS,
        )
    return InMemoryEventBus(
        name='InMemoryEventBus'
    )


def get_source():
    return os.environ['EVENT_SOURCE']


def get_batch_upgrade_started_detail(props):
    return {
        'metadata': {
            'includes_slack_notification': True,
        },
        'data': {
            'slack': {
                'text': f':mega: *BatchUpgradeStarted* | {props.source}'
            }
        }
    }


def get_batch_upgrade_completed_detail(props, result):
    decoded_results = result.stdout.decode('utf-8')[-1000:]
    return {
        'metadata': {
            'includes_slack_notification': True,
        },
        'data': {
            'slack': {
                'text': (
                    f':white_check_mark: *BatchUpgradeCompleted* | {props.source}\n'
                    f'```{decoded_results}```'
                )
            }
        }
    }


def get_batch_upgrade_failed_detail(props, error):
    decoded_error = error.stdout.decode('utf-8')[-1000:]
    return {
        'metadata': {
            'includes_slack_notification': True,
        },
        'data': {
            'slack': {
                'text': (
                    f':x: *BatchUpgradeFailed* | {props.source}\n'
                    f'```{decoded_error}```'
                )
            }
        }
    }


def notify_batch_upgrade_started(props):
    logger.info('Sending BatchUpgradeStarted event')
    logger.info(props.bus.name)
    event = BatchUpgradeStarted(
        source=props.source,
        event_bus_name=props.bus.name,
        detail=get_batch_upgrade_started_detail(props)
    )
    logger.info(event)
    response = props.bus.notify(
        [
            event
        ]
    )
    logger.info(response)


def notify_batch_upgrade_completed(props, result):
    logger.info('Sending BatchUpgradeCompleted event')
    logger.info(props.bus.name)
    event = BatchUpgradeCompleted(
        source=props.source,
        event_bus_name=props.bus.name,
        detail=get_batch_upgrade_completed_detail(props, result)
    )
    logger.info(event)
    response = props.bus.notify(
        [
            event
        ]
    )
    logger.info(response)


def notify_batch_upgrade_failed(props, error):
    logger.info('Sending BatchUpgradeFailed event')
    logger.info(props.bus.name)
    event = BatchUpgradeFailed(
        source=props.source,
        event_bus_name=props.bus.name,
        detail=get_batch_upgrade_failed_detail(props, error)
    )
    logger.info(event)
    response = props.bus.notify(
        [
            event
        ]
    )
    logger.info(response)


def run_batch_upgrade(args):
    command = BATCH_UPGRADE_COMMAND + args
    return run(
        command,
        stdout=PIPE,
        stderr=STDOUT,
        check=True
    )


def run_batch_upgrade_with_event_notification(props, args):
    logger.info('Running batchupgrade with event notification')
    notify_batch_upgrade_started(props)
    try:
        result = run_batch_upgrade(args)
        logger.info(result.stdout.decode('utf-8'))
        notify_batch_upgrade_completed(props, result)
    except CalledProcessError as error:
        logger.info(error.stdout.decode('utf-8'))
        notify_batch_upgrade_failed(props, error)


def main():
    args = sys.argv[1:]
    props = BatchUpgradeNotificationProps(
        bus=get_bus(),
        source=get_source(),
    )
    run_batch_upgrade_with_event_notification(props, args)


if __name__ == '__main__':
    main()
