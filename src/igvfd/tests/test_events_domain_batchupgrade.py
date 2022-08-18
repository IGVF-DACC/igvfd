import pytest


def test_events_domain_batch_upgrade_batch_upgrade_started():
    from igvfd.events.domain.batchupgrade import BatchUpgradeStarted
    event = BatchUpgradeStarted(
        source='xyz',
        detail={
            'some': 'details'
        },
        event_bus_name='zyx',
    )
    assert isinstance(event, BatchUpgradeStarted)
    assert event.name == 'BatchUpgradeStarted'
    assert event.as_entry() == {
        'Source': 'xyz',
        'DetailType': 'BatchUpgradeStarted',
        'Detail': '{"some": "details"}',
        'EventBusName': 'zyx'
    }


def test_events_domain_batch_upgrade_batch_upgrade_completed():
    from igvfd.events.domain.batchupgrade import BatchUpgradeCompleted
    event = BatchUpgradeCompleted(
        source='xyz',
        detail={
            'some': 'details'
        },
        event_bus_name='zyx',
    )
    assert isinstance(event, BatchUpgradeCompleted)
    assert event.name == 'BatchUpgradeCompleted'
    assert event.as_entry() == {
        'Source': 'xyz',
        'DetailType': 'BatchUpgradeCompleted',
        'Detail': '{"some": "details"}',
        'EventBusName': 'zyx'
    }


def test_events_domain_batch_upgrade_batch_upgrade_failed():
    from igvfd.events.domain.batchupgrade import BatchUpgradeFailed
    event = BatchUpgradeFailed(
        source='xyz',
        detail={
            'some': 'details'
        },
        event_bus_name='zyx',
    )
    assert isinstance(event, BatchUpgradeFailed)
    assert event.name == 'BatchUpgradeFailed'
    assert event.as_entry() == {
        'Source': 'xyz',
        'DetailType': 'BatchUpgradeFailed',
        'Detail': '{"some": "details"}',
        'EventBusName': 'zyx'
    }
