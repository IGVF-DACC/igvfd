import pytest

import os

import time


@pytest.fixture
def external_tx():
    pass


def wait_for_indexing():
    time.sleep(45)


def wait_for_indexing_poll(app):
    from webtest import TestApp
    environ = {
        'HTTP_ACCEPT': 'application/json',
        'REMOTE_USER': 'TEST',
    }
    testapp = TestApp(app, environ)
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


@pytest.yield_fixture(scope='session')
def workbook(app, app_settings):
    from igvfd.loadxl import load_test_data
    from snovault.elasticsearch.manage_mappings import manage_mappings
    manage_mappings(app)
    load_test_data(app)
    wait_for_indexing_poll(app)
    yield
