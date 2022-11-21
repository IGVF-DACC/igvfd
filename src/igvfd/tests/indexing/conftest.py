import pytest

import os

import time


@pytest.fixture
def external_tx():
    pass


def wait_for_indexing():
    time.sleep(45)


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
    from snovault.elasticsearch import create_mapping
    load_test_data(app)
    create_mapping.run(app)
    wait_for_indexing()
    yield
