import logging

import os

import sys

from subprocess import run
from subprocess import PIPE
from subprocess import STDOUT
from subprocess import CalledProcessError


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DEFAULT_EVENT_BUS = os.environ.get('DEFAULT_EVENT_BUS')


BATCH_UPGRADE_COMMAND = [
    'batchupgrade',
]


def get_formatted_slack_message_from_batch_upgrade_completed_result(result):
    return {

    }


def notify_batch_upgrade_started():
    logger.info('Sending BatchUpgradeStarted event')
    logger.info(DEFAULT_EVENT_BUS)


def notify_batch_upgrade_completed(result):
    logger.info('Sending BatchUpgradeCompleted event')
    logger.info(DEFAULT_EVENT_BUS)
    batch_upgrade_completed_event = BatchUpgradeCompleted(
        detail=get_formatted_slack_message_from_batch_upgrade_completed_result(
            result
        )
    )
    result = event_bus.notify(
        [
            batch_upgrade_completed_event
        ]
    )
    logger.info(result)


def notify_batch_upgrade_failed(error):
    logger.info('Sending BatchUpgradeFailed event')
    logger.info(DEFAULT_EVENT_BUS)


def run_batch_upgrade(args):
    command = BATCH_UPGRADE_COMMAND + args
    return run(
        command,
        stdout=PIPE,
        stderr=STDOUT,
        check=True
    )


def run_batch_upgrade_with_event_notification(args):
    logger.info('Running batchupgrade with event notification')
    notify_batch_upgrade_started()
    try:
        result = run_batch_upgrade(args)
        logger.info(result.stdout.decode('utf-8'))
        notify_batch_upgrade_completed(result)
    except CalledProcessError as error:
        logger.info(error.stdout.decode('utf-8'))
        notify_batch_upgrade_failed(error)


def main():
    args = sys.argv[1:]
    run_batch_upgrade_with_event_notification(args)


if __name__ == '__main__':
    main()
