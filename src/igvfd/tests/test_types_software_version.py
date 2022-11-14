import pytest


def test_software_version_name(software_version, testapp):
    res = testapp.get(software_version['@id'])
    assert res.json['name'] == 'bowtie2-v2.4.4'


def test_non_unique_software(testapp, software_version):
    res = testapp.post_json(
        '/software_version', software_version, expect_errors=True
    )
    assert res.status_code == 422
