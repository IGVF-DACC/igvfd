import pytest


def test_events_update_mapping_update_mapping_events():
    from infrastructure.events.updatemapping import UpdateMappingEvents
    assert UpdateMappingEvents.MAPPING_CHANGED == 'MappingChanged'
