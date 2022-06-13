import pytest


def test_title(testapp, pi):
    lab = testapp.post_json(
        '/lab',
        {
            'name': 'test-lab',
            'institute_label': 'Stanford',
            'pi': pi['@id']
        },
        status=201
    ).json['@graph'][0]
    assert lab['title'] == 'Principal Investigator, Stanford'
