from dataclasses import dataclass

from igvfd.events.domain.eventbridge import EventBridgeEvent


@dataclass
class BatchUpgradeStarted(EventBridgeEvent):
    pass


@dataclass
class BatchUpgradeCompleted(EventBridgeEvent):
    pass


@dataclass
class BatchUpgradeFailed(EventBridgeEvent):
    pass
