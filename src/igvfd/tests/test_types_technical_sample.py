import pytest


def test_technical_sample_summary(testapp, technical_sample):
    res = testapp.get(technical_sample['@id'])
    assert res.json.get('summary') == 'synthetic technical sample'
