import pytest


def test_open_reading_frame_upgrade_1_2(upgrader, open_reading_frame_v1):
    value = upgrader.upgrade('open_reading_frame', open_reading_frame_v1, current_version='1', target_version='2')
    assert value['notes'] == 'This object does not have award and lab specified previously, it was upgraded to have Cherry lab/award.'
    assert value['lab'] == '/labs/j-michael-cherry'
    assert value['award'] == '/awards/HG012012'
    assert value['schema_version'] == '2'
