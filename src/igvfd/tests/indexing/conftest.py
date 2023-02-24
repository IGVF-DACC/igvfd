import pytest

import os

import time


@pytest.fixture
def external_tx():
    pass


def make_test_app(app):
    from webtest import TestApp
    environ = {
        'HTTP_ACCEPT': 'application/json',
        'REMOTE_USER': 'TEST',
    }
    return TestApp(app, environ)


def wait_for_indexing_poll(testapp):
    double_check_number = 3
    while True:
        print('Waiting for indexing', double_check_number)
        is_indexing = bool(testapp.get('/indexer-info').json['is_indexing'])
        if is_indexing:
            double_check_number = 3
        else:
            double_check_number -= 1
        if double_check_number <= 0:
            break
        time.sleep(10)


def wait_for_opensearch(app):
    import time
    from snovault.elasticsearch.interfaces import ELASTIC_SEARCH
    from snovault.elasticsearch.interfaces import RESOURCES_INDEX
    os = app.registry[ELASTIC_SEARCH]
    attempt = 0
    while True:
        print('Waiting for Opensearch', attempt)
        attempt += 1
        time.sleep(10)
        try:
            os.indices.get('*')
            print('Found Opensearch', attempt)
            break
        except Exception as e:
            print(e)


@pytest.fixture
def poll_until_indexing_is_done():
    return wait_for_indexing_poll


@pytest.fixture(scope='session')
def app_settings(ini_file):
    settings = ini_file.copy()
    settings['elasticsearch.server'] = 'opensearch:9200'
    settings['collection_datastore'] = 'elasticsearch'
    settings['item_datastore'] = 'elasticsearch'
    settings['snovault.elasticsearch.index'] = 'snovault'
    return settings


@pytest.yield_fixture(scope='session')
def app(app_settings):
    from igvfd import main
    app = main({}, **app_settings)
    yield app
    from snovault import DBSESSION
    DBSession = app.registry[DBSESSION]
    # Dispose connections so postgres can tear down.
    DBSession.bind.pool.dispose()


@pytest.yield_fixture(scope='session')
def workbook(app, app_settings):
    from snovault.elasticsearch.manage_mappings import manage_mappings
    from igvfd.loadxl import load_test_data
    testapp = make_test_app(app)
    wait_for_opensearch(app)
    print('Manage mappings')
    manage_mappings(app)
    print('Load data inserts')
    load_test_data(app)
    wait_for_indexing_poll(testapp)
    yield
