import pytest


def test_events_domain_eventbridge_initialize_event_bridge_event():
    from igvfd.events.domain.eventbridge import EventBridgeEvent
    event = EventBridgeEvent(
        source='xyz',
        detail={
            'some': 'details'
        },
        event_bus_name='zyx',
    )
    assert isinstance(event, EventBridgeEvent)
    assert event.source == 'xyz'
    assert event.detail == {
        'some': 'details'
    }
    assert event.event_bus_name == 'zyx'


def test_events_domain_eventbridge_event_bridge_event_name():
    from igvfd.events.domain.eventbridge import EventBridgeEvent
    event = EventBridgeEvent(
        source='xyz',
        detail={
            'some': 'details'
        },
        event_bus_name='zyx',
    )
    assert event.name == 'EventBridgeEvent'


def test_events_domain_eventbridge_event_bridge_as_entry():
    from igvfd.events.domain.eventbridge import EventBridgeEvent
    event = EventBridgeEvent(
        source='xyz',
        detail={
            'some': 'details'
        },
        event_bus_name='zyx',
    )
    assert event.as_entry() == {
        'Source': 'xyz',
        'DetailType': 'EventBridgeEvent',
        'Detail': '{"some": "details"}',
        'EventBusName': 'zyx'
    }
