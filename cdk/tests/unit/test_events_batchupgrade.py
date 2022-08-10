import pytest


def test_events_batch_upgrade_batch_upgrade_events():
    from infrastructure.events.batchupgrade import BatchUpgradeEvents
    assert BatchUpgradeEvents.UPGRADE_FOLDER_CHANGED == 'UpgradeFolderChanged'
