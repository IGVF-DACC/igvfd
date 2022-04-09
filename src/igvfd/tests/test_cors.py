import pytest


def test_cors_is_cors_request():
    from igvfd.cors import is_cors_request
    from pyramid.testing import DummyRequest
    dr = DummyRequest()
    assert not is_cors_request(dr)
    dr = DummyRequest(
        headers={
            'Origin': 'http//:localhost:3000'
        }
    )
    assert is_cors_request(dr)


def test_cors_is_cors_preflight_request():
    from igvfd.cors import is_cors_preflight_request
    from pyramid.testing import DummyRequest
    dr = DummyRequest(
        headers={
            'Origin': 'http//:localhost:3000'
        }
    )
    assert not is_cors_preflight_request(dr)
    dr = DummyRequest(
        method='OPTIONS',
        headers={
            'Origin': 'http//:localhost:3000',
            'Access-Control-Request-Method': 'POST',
        }
    )
    assert not is_cors_preflight_request(dr)
    dr = DummyRequest(
        method='OPTIONS',
        headers={
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Accept,Origin,X-CSRF-Token'
        }
    )
    assert is_cors_preflight_request(dr)


def test_cors_cors_preflight_predicate():
    from igvfd.cors import CorsPreflightPredicate
    from pyramid.testing import DummyRequest
    cpp = CorsPreflightPredicate(False, {})
    assert cpp.val is False
    cpp = CorsPreflightPredicate(True, {})
    assert cpp.val is True
    dr = DummyRequest(
        headers={
            'Origin': 'http//:localhost:3000'
        }
    )
    assert cpp({}, dr) is False
    dr = DummyRequest(
        method='OPTIONS',
        headers={
            'Origin': 'http//:localhost:3000',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Accept,Origin,X-CSRF-Token'
        }
    )
    assert cpp({}, dr) is True


def test_cors_parse_ini_setting_as_list(dummy_request):
    from igvfd.cors import parse_ini_setting_as_list
    assert parse_ini_setting_as_list(
        'http://localhost:3000\nhttp://someother.com'
    ) == [
        'http://localhost:3000',
        'http://someother.com'
    ]
    trusted_origins = dummy_request.registry.settings.get(
        'cors_trusted_origins'
    )
    assert parse_ini_setting_as_list(
        trusted_origins
    ) == [
        'http://localhost:3000'
    ]


def test_cors_get_allowed_origins(dummy_request):
    from igvfd.cors import get_allowed_origins
    assert get_allowed_origins(dummy_request) == [
        'http://localhost:3000',
    ]


def test_cors_origin_is_allowed(dummy_request):
    from igvfd.cors import origin_is_allowed
    dummy_request.headers.update({'Origin': 'http://localhost:3000'})
    assert origin_is_allowed(dummy_request)
    dummy_request.headers.update({'Origin': 'http://localhost:2999'})
    assert not origin_is_allowed(dummy_request)
    original_trusted = dummy_request.registry.settings['cors_trusted_origins']
    dummy_request.registry.settings['cors_trusted_origins'] = ''
    assert not origin_is_allowed(dummy_request)
    dummy_request.registry.settings['cors_trusted_origins'] = (
        'http://localhost:2999'
    )
    assert origin_is_allowed(dummy_request)
    dummy_request.registry.settings['cors_trusted_origins'] = (
        'http://localhost:2999\nhttp://localhost:3000'
    )
    assert origin_is_allowed(dummy_request)
    dummy_request.registry.settings['cors_trusted_origins'] = original_trusted
    assert not origin_is_allowed(dummy_request)


def test_cors_method_is_allowed(dummy_request):
    from igvfd.cors import method_is_allowed
    for method in [
            'GET',
            'POST',
            'PATCH',
            'PUT',
            'OPTIONS',
            'HEAD',
    ]:
        dummy_request.method = method
        assert method_is_allowed(dummy_request)
    for method in [
            'DELETE',
            'OTHER',
    ]:
        dummy_request.method = method
        assert not method_is_allowed(dummy_request)


def test_cors_should_add_cors_to_headers(dummy_request):
    from igvfd.cors import should_add_cors_to_headers
    assert not should_add_cors_to_headers(dummy_request)
    dummy_request.headers.update({'Origin': 'http://localhost:2999'})
    dummy_request.method = 'POST'
    assert not should_add_cors_to_headers(dummy_request)
    dummy_request.headers.update({'Origin': 'http://localhost:3000'})
    dummy_request.method = 'POST'
    assert should_add_cors_to_headers(dummy_request)
    dummy_request.headers.update({'Origin': 'http://localhost:3000'})
    dummy_request.method = 'DELETE'
    assert not should_add_cors_to_headers(dummy_request)


def test_cors_add_allowed_cors_headers_to_response(dummy_request):
    from igvfd.cors import _add_allowed_cors_headers_to_response
    assert 'Access-Control-Allow-Origin' not in dummy_request.response.headers
    assert 'Access-Control-Allow-Credentials' not in dummy_request.response.headers
    assert 'Access-Control-Expose-Headers' not in dummy_request.response.headers
    dummy_request.headers.update(
        {
            'Origin': 'somehost'
        }
    )
    _add_allowed_cors_headers_to_response(dummy_request)
    assert 'Access-Control-Allow-Origin' in dummy_request.response.headers
    assert 'Access-Control-Allow-Credentials' in dummy_request.response.headers
    assert 'Access-Control-Expose-Headers' in dummy_request.response.headers
    assert dummy_request.response.headers['Access-Control-Allow-Origin'] == 'somehost'


def test_cors_add_allowed_preflight_cors_headers_to_response(dummy_request):
    from igvfd.cors import _add_allowed_preflight_cors_headers_to_response
    assert 'Access-Control-Allow-Methods' not in dummy_request.response.headers
    assert 'Access-Control-Allow-Headers' not in dummy_request.response.headers
    _add_allowed_preflight_cors_headers_to_response(dummy_request)
    assert 'Access-Control-Allow-Methods' in dummy_request.response.headers
    assert 'Access-Control-Allow-Headers' in dummy_request.response.headers


def test_cors_update_vary_header_in_response(dummy_request):
    from igvfd.cors import _update_vary_header_in_response
    assert 'Vary' not in dummy_request.response.headers
    dummy_request.response.headers.update(
        {
            'Vary': 'Somthing, Else'
        }
    )
    _update_vary_header_in_response(dummy_request)
    assert 'Vary' in dummy_request.response.headers
    assert 'Origin' in dummy_request.response.headers['Vary']
    assert dummy_request.response.headers['Vary'] == 'Somthing,Else,Origin'


def test_cors_add_cors_to_response_headers(dummy_request):
    from igvfd.cors import _add_cors_to_response_headers
    assert 'Access-Control-Allow-Origin' not in dummy_request.response.headers
    assert 'Access-Control-Allow-Credentials' not in dummy_request.response.headers
    assert 'Access-Control-Expose-Headers' not in dummy_request.response.headers
    assert 'Vary' not in dummy_request.response.headers
    dummy_request.headers.update(
        {
            'Origin': 'somehost'
        }
    )
    _add_cors_to_response_headers(dummy_request)
    assert 'Access-Control-Allow-Origin' in dummy_request.response.headers
    assert 'Access-Control-Allow-Credentials' in dummy_request.response.headers
    assert 'Access-Control-Expose-Headers' in dummy_request.response.headers
    assert dummy_request.response.headers['Access-Control-Allow-Origin'] == 'somehost'
    assert 'Vary' in dummy_request.response.headers
    assert 'Origin' in dummy_request.response.headers['Vary']


def test_cors_maybe_add_cors_to_response_header(dummy_request):
    from igvfd.cors import maybe_add_cors_to_response_headers
    assert 'Access-Control-Allow-Origin' not in dummy_request.response.headers
    assert 'Access-Control-Allow-Credentials' not in dummy_request.response.headers
    assert 'Access-Control-Expose-Headers' not in dummy_request.response.headers
    assert 'Vary' not in dummy_request.response.headers
    dummy_request.headers.update(
        {
            'Origin': 'somehost'
        }
    )
    maybe_add_cors_to_response_headers(dummy_request)
    assert 'Access-Control-Allow-Origin' not in dummy_request.response.headers
    assert 'Access-Control-Allow-Credentials' not in dummy_request.response.headers
    assert 'Access-Control-Expose-Headers' not in dummy_request.response.headers
    assert 'Vary' not in dummy_request.response.headers
    dummy_request.headers.update(
        {
            'Origin': 'http://localhost:3000'
        }
    )
    maybe_add_cors_to_response_headers(dummy_request)
    assert 'Access-Control-Allow-Origin' in dummy_request.response.headers
    assert 'Access-Control-Allow-Credentials' in dummy_request.response.headers
    assert 'Access-Control-Expose-Headers' in dummy_request.response.headers
    assert dummy_request.response.headers['Access-Control-Allow-Origin'] == (
        'http://localhost:3000'
    )
    assert 'Vary' in dummy_request.response.headers
    assert 'Origin' in dummy_request.response.headers['Vary']


def test_cors_maybe_add_preflight_cors_to_response_header(dummy_request):
    from igvfd.cors import maybe_add_preflight_cors_to_response_headers
    assert 'Access-Control-Allow-Methods' not in dummy_request.response.headers
    assert 'Access-Control-Allow-Headers' not in dummy_request.response.headers
    maybe_add_preflight_cors_to_response_headers(dummy_request)
    assert 'Access-Control-Allow-Methods' not in dummy_request.response.headers
    assert 'Access-Control-Allow-Headers' not in dummy_request.response.headers
    dummy_request.method = 'PATCH'
    dummy_request.headers.update(
        {
            'Origin': 'http://evilhost:3000',
            'Access-Control-Request-Method': 'PATCH',
            'Access-Control-Request-Headers': 'Accept,Origin,X-CSRF-Token',
        }
    )
    maybe_add_preflight_cors_to_response_headers(dummy_request)
    assert 'Access-Control-Allow-Methods' not in dummy_request.response.headers
    assert 'Access-Control-Allow-Headers' not in dummy_request.response.headers
    dummy_request.method = 'PATCH'
    dummy_request.headers.update(
        {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'PATCH',
            'Access-Control-Request-Headers': 'Accept,Origin,X-CSRF-Token',
        }
    )
    maybe_add_preflight_cors_to_response_headers(dummy_request)
    assert 'Access-Control-Allow-Methods' in dummy_request.response.headers
    assert 'Access-Control-Allow-Headers' in dummy_request.response.headers


def test_cors_test_handle_cors_preflight_view(testapp):
    response = testapp.options(
        '/login',
        status=404
    )
    headers = {
        'Origin': 'http://evilhost:3000',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Accept,Origin,X-CSRF-Token,Content-Length',
    }
    response = testapp.options(
        '/login',
        headers=headers
    )
    assert response.status_code == 200
    assert 'Access-Control-Allow-Methods' not in response.headers
    assert 'Access-Control-Allow-Headers' not in response.headers
    headers = {
        'Origin': 'http://localhost:3000',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Accept,Origin,X-CSRF-Token,Content-Length',
    }
    response = testapp.options(
        '/someotherview',
        headers=headers
    )
    assert response.status_code == 200
    assert 'Access-Control-Allow-Methods' in response.headers
    assert 'Access-Control-Allow-Headers' in response.headers


def test_cors_maybe_add_cors_to_response_headers_subscriber(testapp):
    response = testapp.get(
        '/session',
    )
    assert 'Content-Type' in response.headers
    assert 'Set-Cookie' in response.headers
    assert 'Vary' in response.headers
    assert 'X-Stats' in response.headers
    assert 'Access-Control-Allow-Origin' not in response.headers
    assert 'Access-Control-Allow-Credentials' not in response.headers
    assert 'Access-Control-Expose-Headers' not in response.headers
    testapp.cookiejar.clear()
    headers = {
        'Origin': 'http://evilhost:3000',
    }
    response = testapp.get(
        '/session',
        headers=headers
    )
    assert 'Content-Type' in response.headers
    assert 'Set-Cookie' in response.headers
    assert 'Vary' in response.headers
    assert 'X-Stats' in response.headers
    assert 'Access-Control-Allow-Origin' not in response.headers
    assert 'Access-Control-Allow-Credentials' not in response.headers
    assert 'Access-Control-Expose-Headers' not in response.headers
    testapp.cookiejar.clear()
    headers = {
        'Origin': 'http://localhost:3000',
    }
    response = testapp.get(
        '/session',
        headers=headers
    )
    assert 'Content-Type' in response.headers
    assert 'Set-Cookie' in response.headers
    assert 'Vary' in response.headers
    assert 'X-Stats' in response.headers
    assert 'Access-Control-Allow-Origin' in response.headers
    assert 'Access-Control-Allow-Credentials' in response.headers
    assert 'Access-Control-Expose-Headers' in response.headers
    assert response.headers['Access-Control-Allow-Origin'] == 'http://localhost:3000'
    assert response.headers['Vary'] == 'Origin, Accept, Authorization'
    assert response.headers['Access-Control-Allow-Credentials'] == 'true'
