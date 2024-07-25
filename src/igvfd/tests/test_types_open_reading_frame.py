import pytest


def test_open_reading_frame_summary(testapp, orf_foxp):
    res = testapp.get(orf_foxp['@id'])
    assert res.json.get('summary', '') == 'CCSBORF1234 of MYC - ENSP00000001146.2'
