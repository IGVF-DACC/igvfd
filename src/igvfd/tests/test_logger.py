import datetime
from types import SimpleNamespace

import pytest

from gunicorn.config import Config
from igvfd.logging.gunicornlogger import MyGunicornLogger
from igvfd.logging.gunicornlogger import try_to_convert_to_int


def test_no_x_stats():
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
    assert atoms['x'] == -1


def test_two_x_stat_tokens():
    response = SimpleNamespace(
        status='200', response_length=1024,
        headers=(
            ('Content-Type', 'application/json'),
            ('X-Stats', 'x=y&foo=42'),
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
    assert atoms['x'] == -1
    assert atoms['foo'] == 42


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


def test_try_to_convert_to_int_int():
    result = try_to_convert_to_int('42')
    assert result == 42


def test_try_to_convert_to_int_not_int():
    result = try_to_convert_to_int('foo')
    assert result == -1
