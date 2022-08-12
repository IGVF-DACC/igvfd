import pytest


def test_events_naming_get_event_source_from_config(config):
    from infrastructure.events.naming import get_event_source_from_config
    assert get_event_source_from_config(config) == 'igvfd.demo.some-branch'
