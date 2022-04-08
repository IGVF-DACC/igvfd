import os
import pytest
import pkg_resources
import tempfile

from pyramid.paster import get_appsettings


tempfile.tempdir = '/tmp'

pytest_plugins = [
    'igvfd.tests.fixtures.database',
    'igvfd.tests.fixtures.testapp',
    'igvfd.tests.fixtures.alias',
    'igvfd.tests.fixtures.pyramid',
    'igvfd.tests.fixtures.schemas.access_key',
    'igvfd.tests.fixtures.schemas.source',
    'igvfd.tests.fixtures.schemas.award',
    'igvfd.tests.fixtures.schemas.lab',
    'igvfd.tests.fixtures.schemas.cell_line',
    'igvfd.tests.fixtures.schemas.user',
]


@pytest.fixture(scope='session')
def ini_file(request):
    path = os.path.abspath(
        request.config.option.ini or 'config/pyramid/ini/testing.ini'
    )
    return get_appsettings(path, name='app')


@pytest.fixture(autouse=True)
def autouse_external_tx(external_tx):
    pass


@pytest.fixture(scope='session')
def app_settings(ini_file, DBSession):
    from snovault import DBSESSION
    ini_file[DBSESSION] = DBSession
    return ini_file


@pytest.fixture(scope='session')
def app(app_settings):
    from igvfd import main
    return main({}, **app_settings)


@pytest.fixture(scope='session')
def workbook(conn, app, app_settings):
    tx = conn.begin_nested()
    try:
        from igvfd.loadxl import load_test_data
        load_test_data(app)
        yield
    finally:
        tx.rollback()
