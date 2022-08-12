import json

from dataclasses import dataclass

from typing import Dict
from typing import Any


@dataclass
class EventBridgeEvent:
    source: str
    detail: Dict[str, Any]
    event_bus_name: str

    @property
    def name(self):
        return type(self).__name__

    def as_entry(self):
        return {
            'Source': self.source,
            'DetailType': self.name,
            'Detail': json.dumps(self.detail),
            'EventBusName': self.event_bus_name,
        }
