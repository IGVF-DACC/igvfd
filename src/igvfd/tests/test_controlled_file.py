import pytest


def _remote_user_testapp(app, remote_user):
    from webtest import TestApp
    environ = {
        'HTTP_ACCEPT': 'application/json',
        'REMOTE_USER': str(remote_user),
    }
    return TestApp(app, environ)


@pytest.fixture
def remote_user_testapp(app, remote_user):
    return _remote_user_testapp(app, remote_user)


@pytest.fixture
def wrangler_testapp(wrangler, app, external_tx, zsa_savepoints):
    return _remote_user_testapp(app, wrangler['uuid'])


@pytest.fixture
def submitter_testapp(submitter, app, external_tx, zsa_savepoints):
    return _remote_user_testapp(app, submitter['uuid'])


def test_submitter_post_controlled_access_file(submitter_testapp, controlled_sequence_file):
    submitter_testapp.post_json('/sequence_file', controlled_sequence_file, status=201)


def test_wrangler_post_controlled_access_file(wrangler_testapp, controlled_sequence_file):
    wrangler_testapp.post_json('/sequence_file', controlled_sequence_file, status=201)


def test_submitter_put_controlled_access_file(submitter_testapp, controlled_sequence_file_object):
    controlled_sequence_file = submitter_testapp.get(controlled_sequence_file_object['@id'] + '@@edit').json
    controlled_sequence_file['controlled_access'] = False
    submitter_testapp.put_json(controlled_sequence_file_object['@id'], controlled_sequence_file, status=422)


def test_wrangler_put_controlled_access_file(wrangler_testapp, controlled_sequence_file_object):
    controlled_sequence_file = wrangler_testapp.get(controlled_sequence_file_object['@id'] + '@@edit').json
    controlled_sequence_file['controlled_access'] = False
    wrangler_testapp.put_json(controlled_sequence_file_object['@id'], controlled_sequence_file, status=422)


def test_submitter_patch_controlled_access_file(submitter_testapp, controlled_sequence_file_object):
    res = submitter_testapp.get(controlled_sequence_file_object['@id'])
    controlled_access = {'controlled_access': False}
    submitter_testapp.patch_json(res.json['@id'], controlled_access, status=422)


def test_wrangler_patch_controlled_access_file(wrangler_testapp, controlled_sequence_file_object):
    res = wrangler_testapp.get(controlled_sequence_file_object['@id'])
    controlled_access = {'controlled_access': False}
    wrangler_testapp.patch_json(res.json['@id'], controlled_access, status=422)
