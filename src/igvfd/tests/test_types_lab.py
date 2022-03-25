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
    assert(lab['title']) == 'Principal Investigator, Stanford'


def test_bad_lab(testapp, pi):
    testapp.post_json(
        '/lab',
        {
            'name': 'bad-lab',
            'institute_label': 'Stanford'
        },
        status=422)
