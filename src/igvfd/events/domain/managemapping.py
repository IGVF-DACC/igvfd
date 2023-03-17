from dataclasses import dataclass

from igvfd.events.domain.eventbridge import EventBridgeEvent


@dataclass
class ManageMappingStarted(EventBridgeEvent):
    pass


@dataclass
class ManageMappingCompleted(EventBridgeEvent):
    pass


@dataclass
class ManageMappingFailed(EventBridgeEvent):
    pass
