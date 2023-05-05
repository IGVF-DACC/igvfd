import pytest


def test_start_view_position_regex(testapp, signal_file):
    res = testapp.patch_json(
        signal_file['@id'],
        {
            'start_view_position': 'chr01:54362'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        signal_file['@id'],
        {
            'start_view_position': 'chr23:54362'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        signal_file['@id'],
        {
            'start_view_position': 'chrX:54362'
        })
    assert res.status_code == 200
    res = testapp.patch_json(
        signal_file['@id'],
        {
            'start_view_position': 'chr3:54362'
        })
    assert res.status_code == 200
    res = testapp.patch_json(
        signal_file['@id'],
        {
            'start_view_position': 'chr20:54362'
        })
    assert res.status_code == 200
