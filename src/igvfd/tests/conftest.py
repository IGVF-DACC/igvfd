import pytest
import pkg_resources

from pyramid.paster import get_appsettings


pytest_plugins = []


def pytest_addoption(parser):
    parser.addoption('--ini', action='store', metavar='INI_FILE')


@pytest.fixture(scope='session')
def ini_file(request):
    return os.path.abspath(
        request.config.option.ini or 'config/pyramid/ini/local.ini'
    )


@pytest.fixture(scope='session')
def app_settings(ini_file):
    return get_appsettings(ini_file)
