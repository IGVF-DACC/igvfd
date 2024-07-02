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


def test_lab_summary(testapp, other_lab):
    res = testapp.get(other_lab['@id'])
    assert res.json.get('summary', '') == 'IGVF VerifiedMember, Other Institute'
