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


@pytest.fixture
def viewing_group_member_testapp(viewing_group_member, app, external_tx, zsa_savepoints):
    return _remote_user_testapp(app, viewing_group_member['uuid'])


@pytest.fixture
def verified_member_testapp(verified_member, app, external_tx, zsa_savepoints):
    return _remote_user_testapp(app, verified_member['uuid'])


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


def test_controlled_file_only_viewing_group_members_can_download_controlled_access_file(testapp, anontestapp, authenticated_testapp, submitter_testapp, viewing_group_member_testapp, verified_member_testapp, controlled_access_alignment_file, alignment_file):
    res = testapp.get(alignment_file['@id'])
    assert res.json['controlled_access'] is False
    assert 's3_uri' in res.json
    assert 'href' in res.json
    assert 'anvil_url' not in res.json
    res = testapp.get(controlled_access_alignment_file['@id'])
    assert res.json['controlled_access'] is True
    assert res.json['status'] == 'in progress'
    assert 's3_uri' in res.json
    assert 'href' in res.json
    assert 'anvil_url' not in res.json
    # Get upload only submitter or admin
    testapp.get(controlled_access_alignment_file['@id'] + '@@upload', status=200)
    submitter_testapp.get(controlled_access_alignment_file['@id'] + '@@upload', status=200)
    authenticated_testapp.get(controlled_access_alignment_file['@id'] + '@@upload', status=403)
    anontestapp.get(controlled_access_alignment_file['@id'] + '@@upload', status=403)
    # Post upload only submitter or admin
    testapp.post_json(controlled_access_alignment_file['@id'] + '@@upload', {}, status=200)
    submitter_testapp.post_json(controlled_access_alignment_file['@id'] + '@@upload', {}, status=200)
    # Not viewing group or anon.
    authenticated_testapp.post_json(controlled_access_alignment_file['@id'] + '@@upload', {}, status=403)
    viewing_group_member_testapp.post_json(controlled_access_alignment_file['@id'] + '@@upload', {}, status=403)
    verified_member_testapp.post_json(controlled_access_alignment_file['@id'] + '@@upload', {}, status=403)
    # Download in progress only if viewing group.
    testapp.get(controlled_access_alignment_file['@id'] + '@@download', status=307)
    authenticated_testapp.get(controlled_access_alignment_file['@id'] + '@@download', status=307)
    submitter_testapp.get(controlled_access_alignment_file['@id'] + '@@download', status=307)
    viewing_group_member_testapp.get(controlled_access_alignment_file['@id'] + '@@download', status=307)
    # Not anon or verified user.
    anontestapp.get(controlled_access_alignment_file['@id'] + '@@download', status=403)
    verified_member_testapp.get(controlled_access_alignment_file['@id'] + '@@download', status=403)
    # Also can't read in progress file metadata unless admin/viewing group.
    testapp.get(controlled_access_alignment_file['@id'], status=200)
    viewing_group_member_testapp.get(controlled_access_alignment_file['@id'], status=200)
    anontestapp.get(controlled_access_alignment_file['@id'], status=403)
    verified_member_testapp.get(controlled_access_alignment_file['@id'], status=403)
    testapp.patch_json(
        controlled_access_alignment_file['@id'],
        {
            'status': 'released',
            'release_timestamp':  '2024-03-06T12:34:56Z',
            'upload_status': 'validated',
        },
        status=200
    )
    res = testapp.get(controlled_access_alignment_file['@id'])
    assert res.json['controlled_access'] is True
    assert res.json['status'] == 'released'
    # Download released
    testapp.get(controlled_access_alignment_file['@id'] + '@@download', status=307)
    authenticated_testapp.get(controlled_access_alignment_file['@id'] + '@@download', status=307)
    submitter_testapp.get(controlled_access_alignment_file['@id'] + '@@download', status=307)
    viewing_group_member_testapp.get(controlled_access_alignment_file['@id'] + '@@download', status=307)
    # Not anon or verified user.
    anontestapp.get(controlled_access_alignment_file['@id'] + '@@download', status=403)
    r = verified_member_testapp.get(controlled_access_alignment_file['@id'] + '@@download', status=403)
    assert r.json['detail'] == 'Downloading controlled-access file not allowed.'
    # All can read released file metadata.
    testapp.get(controlled_access_alignment_file['@id'], status=200)
    viewing_group_member_testapp.get(controlled_access_alignment_file['@id'], status=200)
    anontestapp.get(controlled_access_alignment_file['@id'], status=200)
    verified_member_testapp.get(controlled_access_alignment_file['@id'], status=200)
