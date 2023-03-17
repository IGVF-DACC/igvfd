import logging

import os

from igvfd.events.remote.bus import InMemoryEventBus
from igvfd.events.remote.bus import EventBridgeEventBus

from igvfd.events.domain.managemapping import ManageMappingStarted
from igvfd.events.domain.managemapping import ManageMappingCompleted
from igvfd.events.domain.managemapping import ManageMappingFailed

from dataclasses import dataclass

from typing import Union


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ManageMappingNotificationProps:
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


def get_manage_mapping_started_detail(props):
    return {
        'metadata': {
            'includes_slack_notification': True,
        },
        'data': {
            'slack': {
                'text': f':mega: *ManageMappingStarted* | {props.source}'
            }
        }
    }


def get_manage_mapping_completed_detail(props, summary):
    return {
        'metadata': {
            'includes_slack_notification': True,
        },
        'data': {
            'slack': {
                'text': (
                    f':white_check_mark: *ManageMappingCompleted* | {props.source}\n'
                    f'```{summary}```'
                )
            }
        }
    }


def get_manage_mapping_failed_detail(props):
    return {
        'metadata': {
            'includes_slack_notification': True,
        },
        'data': {
            'slack': {
                'text': (
                    f':x: *ManageMappingFailed* | {props.source}\n'
                )
            }
        }
    }


def notify_manage_mapping_started(props):
    logger.info('Sending ManageMappingStarted event')
    logger.info(props.bus.name)
    event = ManageMappingStarted(
        source=props.source,
        event_bus_name=props.bus.name,
        detail=get_manage_mapping_started_detail(props)
    )
    logger.info(event)
    response = props.bus.notify(
        [
            event
        ]
    )
    logger.info(response)


def notify_manage_mapping_completed(props, summary):
    logger.info('Sending ManageMappingCompleted event')
    logger.info(props.bus.name)
    event = ManageMappingCompleted(
        source=props.source,
        event_bus_name=props.bus.name,
        detail=get_manage_mapping_completed_detail(props, summary)
    )
    logger.info(event)
    response = props.bus.notify(
        [
            event
        ]
    )
    logger.info(response)


def notify_manage_mapping_failed(props, error):
    logger.info('Sending ManageMappingFailed event')
    logger.info(props.bus.name)
    event = ManageMappingFailed(
        source=props.source,
        event_bus_name=props.bus.name,
        detail=get_manage_mapping_failed_detail(props)
    )
    logger.info(event)
    response = props.bus.notify(
        [
            event
        ]
    )
    logger.info(response)


def run_manage_mapping_with_event_notification(props, args):
    from pyramid.paster import get_app
    from snovault.elasticsearch.manage_mappings import manage_mappings
    logger.info('Running manage-mapping with event notification')
    notify_manage_mapping_started(props)
    try:
        app = get_app(
            args.config_uri,
            args.app_name
        )
        summary = manage_mappings(
            app=app,
            relative_mapping_directory=args.relative_mapping_directory,
            should_reindex=args.should_reindex
        )
        logger.info(summary)
        notify_manage_mapping_completed(props, summary)
    except Exception as error:
        notify_manage_mapping_failed(props, error)


def main():
    from snovault.elasticsearch.manage_mappings import get_args
    args = get_args()
    props = ManageMappingNotificationProps(
        bus=get_bus(),
        source=get_source(),
    )
    run_manage_mapping_with_event_notification(props, args)


if __name__ == '__main__':
    main()
