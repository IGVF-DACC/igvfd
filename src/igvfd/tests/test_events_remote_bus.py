import pytest

from moto import mock_events


def test_events_remote_bus_initialize_in_memory_event_bus():
    from igvfd.events.remote.bus import InMemoryEventBus
    from igvfd.events.domain.eventbridge import EventBridgeEvent
    bus = InMemoryEventBus(name='SomeBus')
    assert isinstance(bus, InMemoryEventBus)
    assert bus.name == 'SomeBus'
    event = EventBridgeEvent(
        source='xyz',
        detail={
            'some': 'details'
        },
        event_bus_name='zyx',
    )
    response = bus.notify(
        [event]
    )
    assert response == [
        {
            'Source': 'xyz',
            'DetailType': 'EventBridgeEvent',
            'Detail': '{"some": "details"}',
            'EventBusName': 'zyx'
        }
    ]
    bus.notify([event])
    assert bus._event_bus == [
        {
            'Source': 'xyz',
            'DetailType': 'EventBridgeEvent',
            'Detail': '{"some": "details"}',
            'EventBusName': 'zyx'
        },
        {
            'Source': 'xyz',
            'DetailType': 'EventBridgeEvent',
            'Detail': '{"some": "details"}',
            'EventBusName': 'zyx'
        }
    ]


@mock_events
def test_events_remote_bus_initialize_event_bridge_event_bus(aws_credentials):
    from igvfd.events.remote.bus import EventBridgeEventBus
    from igvfd.events.domain.batchupgrade import BatchUpgradeStarted
    bus = EventBridgeEventBus(name='SomeBus')
    assert isinstance(bus, EventBridgeEventBus)
    assert bus.name == 'SomeBus'
    event = BatchUpgradeStarted(
        source='xyz',
        detail={
            'some': 'details'
        },
        event_bus_name='zyx',
    )
    response = bus.notify(
        [event]
    )
    # EventId unique every time.
    assert len(response['Entries']) == 1
    assert 'EventId' in response['Entries'][0]
    del response['Entries']
    assert response == {
        'FailedEntryCount': 0,
        'ResponseMetadata': {
            'HTTPStatusCode': 200,
            'HTTPHeaders': {
                'server': 'amazon.com'
            },
            'RetryAttempts': 0
        }
    }
