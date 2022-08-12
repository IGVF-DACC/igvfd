import boto3


class InMemoryEventBus:

    def __init__(self, *args, **kwargs):
        self._event_bus = []

    def notify(self, events):
        self._event_bus.extend(
            events
        )


class EventBridgeEventBus:

    def __init__(self, *args, **kwargs):
        self._client = boto3.client('events')

    def notify(self, events):
        return self._client.put_events(
            Entries=[
                event.as_entry()
                for event in events
            ]
        )
