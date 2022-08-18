import pytest

from unittest import mock

from moto import mock_events


@mock_events
def test_commands_batchupgrade_with_notifications_get_bus(aws_credentials):
    from igvfd.commands.batchupgrade_with_notification import get_bus
    from igvfd.events.remote.bus import InMemoryEventBus
    from igvfd.events.remote.bus import EventBridgeEventBus
    bus = get_bus()
    assert isinstance(bus, InMemoryEventBus)
    with mock.patch.dict('os.environ', {'DEFAULT_EVENT_BUS': 'xyz'}):
        bus = get_bus()
        assert isinstance(bus, EventBridgeEventBus)
        assert bus.name == 'xyz'


def test_commands_batchupgrade_with_notifications_get_source():
    from igvfd.commands.batchupgrade_with_notification import get_source
    with mock.patch.dict('os.environ', {'EVENT_SOURCE': 'some-source.app'}, clear=True):
        source = get_source()
        assert source == 'some-source.app'


def test_commands_batchupgrade_with_notifications_get_batch_upgrade_started_detail():
    from igvfd.events.remote.bus import InMemoryEventBus
    from igvfd.commands.batchupgrade_with_notification import BatchUpgradeNotificationProps
    from igvfd.commands.batchupgrade_with_notification import get_batch_upgrade_started_detail
    props = BatchUpgradeNotificationProps(
        bus=InMemoryEventBus(name='xyz'),
        source='some.source',
    )
    detail = get_batch_upgrade_started_detail(props)
    assert detail == {
        'metadata': {
            'includes_slack_notification': True
        },
        'data': {
            'slack': {
                'text': ':mega: *BatchUpgradeStarted* | some.source'
            }
        }
    }


def test_commands_batchupgrade_with_notifications_get_batch_upgrade_completed_detail(mocker):
    from igvfd.events.remote.bus import InMemoryEventBus
    from igvfd.commands.batchupgrade_with_notification import get_batch_upgrade_completed_detail
    from igvfd.commands.batchupgrade_with_notification import BatchUpgradeNotificationProps
    result = mocker.Mock()
    result.stdout = b'some\nkind\nof\nresult'
    props = BatchUpgradeNotificationProps(
        bus=InMemoryEventBus(name='xyz'),
        source='some.source',
    )
    detail = get_batch_upgrade_completed_detail(props, result)
    assert detail == {
        'metadata': {
            'includes_slack_notification': True
        },
        'data': {
            'slack': {
                'text': ':white_check_mark: *BatchUpgradeCompleted* | some.source\n```some\nkind\nof\nresult```'
            }
        }
    }


def test_commands_batchupgrade_with_notifications_get_batch_upgrade_failed_detail(mocker):
    from igvfd.events.remote.bus import InMemoryEventBus
    from igvfd.commands.batchupgrade_with_notification import get_batch_upgrade_failed_detail
    from igvfd.commands.batchupgrade_with_notification import BatchUpgradeNotificationProps
    error = mocker.Mock()
    error.stdout = b'some\nkind\nof\nerror'
    props = BatchUpgradeNotificationProps(
        bus=InMemoryEventBus(name='xyz'),
        source='some.source',
    )
    detail = get_batch_upgrade_failed_detail(props, error)
    assert detail == {
        'metadata': {
            'includes_slack_notification': True
        },
        'data': {
            'slack': {
                'text': ':x: *BatchUpgradeFailed* | some.source\n```some\nkind\nof\nerror```'
            }
        }
    }


@mock_events
def test_commands_batchupgrade_with_notifications_notify_batch_upgrade_started(aws_credentials, caplog):
    import logging
    from igvfd.events.remote.bus import InMemoryEventBus
    from igvfd.commands.batchupgrade_with_notification import BatchUpgradeNotificationProps
    from igvfd.commands.batchupgrade_with_notification import notify_batch_upgrade_started
    props = BatchUpgradeNotificationProps(
        bus=InMemoryEventBus(name='xyz'),
        source='some.source',
    )
    with caplog.at_level(logging.INFO):
        notify_batch_upgrade_started(props)
    assert 'Sending BatchUpgradeStarted event' in caplog.text


@mock_events
def test_commands_batchupgrade_with_notifications_notify_batch_upgrade_completed(aws_credentials, caplog, mocker):
    import logging
    from igvfd.events.remote.bus import InMemoryEventBus
    from igvfd.commands.batchupgrade_with_notification import BatchUpgradeNotificationProps
    from igvfd.commands.batchupgrade_with_notification import notify_batch_upgrade_completed
    props = BatchUpgradeNotificationProps(
        bus=InMemoryEventBus(name='xyz'),
        source='some.source',
    )
    result = mocker.Mock()
    result.stdout = b'some\nkind\nof\nresult'
    with caplog.at_level(logging.INFO):
        notify_batch_upgrade_completed(props, result)
    assert 'Sending BatchUpgradeCompleted event' in caplog.text


@mock_events
def test_commands_batchupgrade_with_notifications_notify_batch_upgrade_failed(aws_credentials, caplog, mocker):
    import logging
    from igvfd.events.remote.bus import InMemoryEventBus
    from igvfd.commands.batchupgrade_with_notification import BatchUpgradeNotificationProps
    from igvfd.commands.batchupgrade_with_notification import notify_batch_upgrade_failed
    props = BatchUpgradeNotificationProps(
        bus=InMemoryEventBus(name='xyz'),
        source='some.source',
    )
    result = mocker.Mock()
    result.stdout = b'some\nkind\nof\nresult'
    with caplog.at_level(logging.INFO):
        notify_batch_upgrade_failed(props, result)
    assert 'Sending BatchUpgradeFailed event' in caplog.text
