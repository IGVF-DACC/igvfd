import pytest


@pytest.fixture
def disabled_user(testapp, lab):
    item = {
        'first_name': 'IGVF',
        'last_name': 'Submitter',
        'email': 'no_login_submitter@example.org',
        'submits_for': [lab['@id']],
        'status': 'disabled',
    }
    res = testapp.post_json('/user', item)
    return testapp.get(res.location).json


@pytest.fixture
def user_0():
    return {
        'first_name': 'Benjamin',
        'last_name': 'Hitz',
        'email': 'hitz@stanford.edu',
    }


@pytest.fixture
def user_v1(user_0):
    item = user_0.copy()
    item.update({
        'schema_version': '1',
        'viewing_groups': ['IGVF'],
        'groups': ['admin', 'verified', 'wrangler'],
        'submits_for': [],
        'aliases': [],
        'groups': []
    })
    return item


@pytest.fixture
def admin(testapp):
    item = {
        'first_name': 'Test',
        'last_name': 'Admin',
        'email': 'admin@example.org',
        'groups': ['admin'],
    }
    res = testapp.post_json('/user', item)
    return testapp.get(res.location).json


@pytest.fixture
def wrangler(testapp):
    item = {
        'uuid': '4c23ec32-c7c8-4ac0-affb-04befcc881d4',
        'first_name': 'Wrangler',
        'last_name': 'Admin',
        'email': 'wrangler@example.org',
        'groups': ['admin'],
    }
    res = testapp.post_json('/user', item)
    return testapp.get(res.location).json


@pytest.fixture
def verified_member(testapp, award):
    item = {
        'first_name': 'IGVF',
        'last_name': 'VerifiedMember',
        'email': 'verified_member@example.org',
        'groups': ['verified'],
    }
    res = testapp.post_json('/user', item)
    return testapp.get(res.location).json


@pytest.fixture
def unverified_member(testapp, award):
    item = {
        'first_name': 'IGVF',
        'last_name': 'NonVerifiedMember',
        'email': 'non_verified_member@example.org',
    }
    # User @@object view has keys omitted.
    res = testapp.post_json('/user', item)
    return testapp.get(res.location).json


@pytest.fixture
def submitter(testapp, lab, award):
    item = {
        'first_name': 'IGVF',
        'last_name': 'Submitter',
        'email': 'igvf_submitter@example.org',
        'submits_for': [lab['@id']],
        'viewing_groups': [award['viewing_group']],
    }
    res = testapp.post_json('/user', item)
    return testapp.get(res.location).json


@pytest.fixture
def pi(testapp):
    item = {
        'first_name': 'Principal',
        'last_name': 'Investigator',
        'email': 'pi@example.org',
        'groups': ['verified'],
    }
    res = testapp.post_json('/user', item)
    return testapp.get(res.location).json


@pytest.fixture
def viewing_group_member(testapp, award):
    item = {
        'first_name': 'Viewing',
        'last_name': 'Group',
        'email': 'viewing_group_member@example.org',
        'viewing_groups': [award['viewing_group']],
    }
    # User @@object view has keys omitted.
    res = testapp.post_json('/user', item)
    return testapp.get(res.location).json


@pytest.fixture
def user_v2(user_v1):
    item = user_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item


@pytest.fixture
def user_v3(user_v1):
    item = user_v1.copy()
    item.update({
        'schema_version': '2',
        'viewing_groups': []
    })
    return item


@pytest.fixture
def user_v4(user_v1):
    item = user_v1.copy()
    item.update({
        'schema_version': '4',
        'email': 'email_name@email_domain.com '
    })
    return item


@pytest.fixture
def user_v5(user_v1):
    item = user_v1.copy()
    item.update(
        {
            'schema_version': '5',
            'email': 'SOME_CAPITAL_EMAIL@cs.EDU.gov',
        }
    )
    return item
