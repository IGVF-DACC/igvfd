import os
import pytest
import pkg_resources

from pyramid.paster import get_appsettings


pytest_plugins = [
    'igvfd.tests.fixtures.database',
    'igvfd.tests.fixtures.testapp',
    'igvfd.tests.fixtures.alias',
    'igvfd.tests.fixtures.pyramid',
]


@pytest.fixture(scope='session')
def ini_file(request):
    return os.path.abspath(
        request.config.option.ini or 'config/pyramid/ini/testing.ini'
    )


@pytest.fixture(autouse=True)
def autouse_external_tx(external_tx):
    pass


@pytest.fixture(scope='session')
def app_settings(ini_file):
    return get_appsettings(ini_file, name='app')


@pytest.fixture(scope='session')
def app(app_settings):
    from igvfd import main
    settings = app_settings.copy()
    return main({}, **app_settings)


@pytest.fixture(scope='session')
def workbook(app, app_settings, conn):
    tx = conn.begin_nested()
    try:
        from igvfd.loadxl import load_test_data
        load_test_data(app)
        yield
    finally:
        tx.rollback()
