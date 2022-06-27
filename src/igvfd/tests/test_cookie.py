import pytest


def test_cookie_generate_hash():
    from igvfd.cookie import generate_hash
    actual = generate_hash(b'123')
    expected = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
    assert actual == expected
    actual = generate_hash(b'abcdefghijstA1')
    expected = '45235dfb24901383e55d84e878681449f13c5b9aa69903883ef422d17e5b1f55'
    assert actual == expected


def test_cookie_get_last_six_bytes_of_secret():
    from igvfd.cookie import get_last_six_bytes_of_secret
    actual = get_last_six_bytes_of_secret(
        'abcdefghijklmnopqrstuvwxyz'
    )
    expected = b'uvwxyz'
    assert actual == expected
    actual = get_last_six_bytes_of_secret(
        b'123abcdefghijklmnopqrstuvwxyz'
    )
    expected = b'uvwxyz'
    assert actual == expected


def test_cookie_generate_cookie_name():
    from igvfd.cookie import generate_cookie_name
    actual = generate_cookie_name(
        'abcdefghijklmnopqrstuvwxyz'
    )
    expected = 'session-5347f5b986'
    assert actual == expected


def test_cookie_add_session_cookie_name_to_settings(dummy_request):
    from igvfd.cookie import add_session_cookie_name_to_settings
    add_session_cookie_name_to_settings(
        dummy_request.registry.settings,
        'abcdefghijklmnopqrstuvwxyz',
    )
    assert 'session_cookie_name' in dummy_request.registry.settings
    assert dummy_request.registry.settings['session_cookie_name'] == 'session-5347f5b986'


def test_cookie_session_cookie_name_view(testapp):
    response = testapp.get('/session-cookie-name')
    data = response.json
    assert 'name' in data
    assert data['name'].startswith('session')
    assert len(data['name']) == 18
