import pytest


def test_software_summary(testapp, software):
    res = testapp.get(software['@id'])
    assert res.json['summary'] == 'Bowtie2'
