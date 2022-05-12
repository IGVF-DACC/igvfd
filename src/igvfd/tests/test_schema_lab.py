import pytest


def test_post_bad_lab(testapp, pi):
    testapp.post_json(
        '/lab',
        {
            'name': 'bad-lab',
            'institute_label': 'Stanford'
        },
        status=422)
