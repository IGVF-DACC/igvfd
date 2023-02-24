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
    load_test_data(app)
    manage_mappings(app)
    wait_for_indexing_poll(testapp)
    yield
