import datetime
from types import SimpleNamespace

import pytest

from gunicorn.config import Config
from igvfd.logging.gunicornlogger import MyGunicornLogger


def test_atoms_no_x_stats():
    response = SimpleNamespace(
        status='200', response_length=1024,
        headers=(('Content-Type', 'application/json'),),
        sent=1024,
    )
    request = SimpleNamespace(headers=(('Accept', 'application/json'),))
    environ = {
        'REQUEST_METHOD': 'GET', 'RAW_URI': '/my/path?foo=bar',
        'PATH_INFO': '/my/path', 'QUERY_STRING': 'foo=bar',
        'SERVER_PROTOCOL': 'HTTP/1.1',
    }
    logger = MyGunicornLogger(Config())
    atoms = logger.atoms(response, request, environ, datetime.timedelta(seconds=1))
    assert isinstance(atoms, dict)
    assert '{content-type}o' in atoms
    assert '{server_protocol}e' in atoms


def test_one_x_stat_token():
    response = SimpleNamespace(
        status='200', response_length=1024,
        headers=(
            ('Content-Type', 'application/json'),
            ('X-Stats', 'x=y'),
        ),
        sent=1024,
    )
    request = SimpleNamespace(headers=(('Accept', 'application/json'),))
    environ = {
        'REQUEST_METHOD': 'GET', 'RAW_URI': '/my/path?foo=bar',
        'PATH_INFO': '/my/path', 'QUERY_STRING': 'foo=bar',
        'SERVER_PROTOCOL': 'HTTP/1.1',
    }
    logger = MyGunicornLogger(Config())
    atoms = logger.atoms(response, request, environ, datetime.timedelta(seconds=1))
    assert '{x-stats}o' in atoms
    assert atoms['x'] == 'y'


def test_two_x_stat_tokens():
    response = SimpleNamespace(
        status='200', response_length=1024,
        headers=(
            ('Content-Type', 'application/json'),
            ('X-Stats', 'x=y&foo=bar'),
        ),
        sent=1024,
    )
    request = SimpleNamespace(headers=(('Accept', 'application/json'),))
    environ = {
        'REQUEST_METHOD': 'GET', 'RAW_URI': '/my/path?foo=bar',
        'PATH_INFO': '/my/path', 'QUERY_STRING': 'foo=bar',
        'SERVER_PROTOCOL': 'HTTP/1.1',
    }
    logger = MyGunicornLogger(Config())
    atoms = logger.atoms(response, request, environ, datetime.timedelta(seconds=1))
    assert atoms['x'] == 'y'
    assert atoms['foo'] == 'bar'


def test_no_x_stat_tokens():
    response = SimpleNamespace(
        status='200', response_length=1024,
        headers=(
            ('Content-Type', 'application/json'),
            ('X-Stats', '-'),
        ),
        sent=1024,
    )
    request = SimpleNamespace(headers=(('Accept', 'application/json'),))
    environ = {
        'REQUEST_METHOD': 'GET', 'RAW_URI': '/my/path?foo=bar',
        'PATH_INFO': '/my/path', 'QUERY_STRING': 'foo=bar',
        'SERVER_PROTOCOL': 'HTTP/1.1',
    }
    logger = MyGunicornLogger(Config())
    atoms = logger.atoms(response, request, environ, datetime.timedelta(seconds=1))
    assert isinstance(atoms, dict)
    assert '{x-stats}o' in atoms
