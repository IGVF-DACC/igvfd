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
            'Origin': 'http//:localhost:3000',
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
