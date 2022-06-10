from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config


def includeme(config):
    config.scan(__name__)
    config.add_route_predicate(
        'cors_preflight',
        CorsPreflightPredicate
    )
    # Globally handle all CORS preflight OPTIONS requests.
    config.add_route(
        'handle-cors-preflight',
        '{match_any:.*}',
        cors_preflight=True,
    )
    config.add_view_deriver(
        maybe_add_cors_to_header_view_deriver
    )


HTTPS_PREFIX = 'https://'

OPTIONS = 'OPTIONS'
GET = 'GET'
POST = 'POST'
PATCH = 'PATCH'
PUT = 'PUT'
HEAD = 'HEAD'

ACCEPT = 'Accept'
CONTENT_TYPE = 'Content-Type'
IF_MATCH = 'If-Match'
ORIGIN = 'Origin'
CACHE_CONTROL = 'Cache-Control'
CONTENT_LANGUAGE = 'Content-Language'
CONTENT_LENGTH = 'Content-Length'
CONTENT_TYPE = 'Content-Type'
EXPIRES = 'Expires'
LAST_MODIFIED = 'Last-Modified'
PRAGMA = 'Pragma'
DATE = 'Date'
TRANSFER_ENCODING = 'Transfer-Encoding'
CONNECTION = 'Connection'
VARY = 'Vary'
X_REQUEST_URL = 'X-Request-Url'
X_STATS = 'X-Stats'
X_CSRF_TOKEN = 'X-CSRF-Token'
X_IF_MATCH_USER = 'X-If-Match-User'

ACCESS_CONTROL_REQUEST_METHOD = 'Access-Control-Request-Method'
ACCESS_CONTROL_REQUEST_HEADERS = 'Access-Control-Request-Headers'

ACCESS_CONTROL_ALLOW_ORIGIN = 'Access-Control-Allow-Origin'
ACCESS_CONTROL_ALLOW_METHODS = 'Access-Control-Allow-Methods'
ACCESS_CONTROL_ALLOW_HEADERS = 'Access-Control-Allow-Headers'
ACCESS_CONTROL_EXPOSE_HEADERS = 'Access-Control-Expose-Headers'
ACCESS_CONTROL_ALLOW_CREDENTIALS = 'Access-Control-Allow-Credentials'
ACCESS_CONTROL_MAX_AGE = 'Access-Control-Max-Age'

ALLOWED_METHODS = [
    GET,
    HEAD,
    OPTIONS,
    POST,
    PATCH,
    PUT,
]

ALLOWED_HEADERS = [
    ORIGIN,
    CONTENT_TYPE,
    ACCEPT,
    X_CSRF_TOKEN,
    X_IF_MATCH_USER,
]

ALLOWED_EXPOSE_HEADERS = [
    CACHE_CONTROL,
    CONTENT_LANGUAGE,
    CONTENT_LENGTH,
    CONTENT_TYPE,
    EXPIRES,
    LAST_MODIFIED,
    PRAGMA,
    DATE,
    TRANSFER_ENCODING,
    CONNECTION,
    X_REQUEST_URL,
    X_STATS,
]

CORS_VARY = (
    ORIGIN,
)


def is_cors_request(request):
    return ORIGIN in request.headers


def is_cors_preflight_request(request):
    return (
        request.method == OPTIONS and
        ORIGIN in request.headers and
        ACCESS_CONTROL_REQUEST_METHOD in request.headers and
        ACCESS_CONTROL_REQUEST_HEADERS in request.headers
    )


class CorsPreflightPredicate(object):
    def __init__(self, val, config):
        self.val = val

    def text(self):
        return f'cors_preflight: {self.val}'

    phash = text

    def __call__(self, context, request):
        if not self.val:
            return False
        return is_cors_preflight_request(request)


def parse_ini_setting_as_list(ini_setting):
    return [
        value.strip()
        for value in ini_setting.split('\n')
        if value
    ]


def get_allowed_origins(request):
    return parse_ini_setting_as_list(
        request.registry.settings.get(
            'cors_trusted_origins',
            ''
        )
    )


def get_allowed_suffixes(request):
    return parse_ini_setting_as_list(
        request.registry.settings.get(
            'cors_trusted_suffixes',
            ''
        )
    )


def origin_matches_exactly(request):
    ALLOWED_ORIGINS = get_allowed_origins(request)
    return ALLOWED_ORIGINS and request.headers.get(ORIGIN) in ALLOWED_ORIGINS


def any_suffixes_match(value, suffixes):
    return any(
        value.endswith(suffix)
        for suffix in suffixes
    )


def origin_matches_suffix(request):
    ALLOWED_SUFFIXES = get_allowed_suffixes(request)
    origin = request.headers.get(ORIGIN, '')
    return (
        ALLOWED_SUFFIXES
        and origin.startswith(HTTPS_PREFIX)
        and any_suffixes_match(origin, ALLOWED_SUFFIXES)
    )


def origin_is_allowed(request):
    # Important for security to limit CORS to trusted origins.
    return (
        origin_matches_exactly(request)
        or origin_matches_suffix(request)
    )


def method_is_allowed(request):
    return request.method in ALLOWED_METHODS


def should_add_cors_to_headers(request):
    return (
        origin_is_allowed(request) and
        method_is_allowed(request)
    )


# Dangerous to call this directly without checking
# if Origin is allowed first.
def _add_allowed_cors_headers_to_response(request):
    origin = request.headers.get(ORIGIN)
    request.response.headers.update(
        {
            ACCESS_CONTROL_ALLOW_ORIGIN: origin,
            ACCESS_CONTROL_ALLOW_CREDENTIALS: 'true',
            ACCESS_CONTROL_EXPOSE_HEADERS: ','.join(ALLOWED_EXPOSE_HEADERS),
        }
    )


def _add_allowed_preflight_cors_headers_to_response(request):
    request.response.headers.update(
        {
            ACCESS_CONTROL_ALLOW_METHODS: ','.join(ALLOWED_METHODS),
            ACCESS_CONTROL_ALLOW_HEADERS: ','.join(ALLOWED_HEADERS),
        }
    )


def _update_vary_header_in_response(request):
    vary = request.response.vary or ()
    request.response.headers.update(
        {
            VARY: ','.join(vary + CORS_VARY)
        }
    )


def _add_cors_to_response_headers(request):
    _add_allowed_cors_headers_to_response(request)
    _update_vary_header_in_response(request)


def maybe_add_cors_to_response_headers(request):
    if should_add_cors_to_headers(request):
        _add_cors_to_response_headers(request)


def maybe_add_preflight_cors_to_response_headers(request):
    if should_add_cors_to_headers(request):
        _add_cors_to_response_headers(request)
        _add_allowed_preflight_cors_headers_to_response(request)


@view_config(
    route_name='handle-cors-preflight',
    request_method='OPTIONS',
    permission=NO_PERMISSION_REQUIRED,
)
def handle_cors_preflight(request):
    maybe_add_preflight_cors_to_response_headers(request)
    return request.response


def maybe_add_cors_to_header_view_deriver(view, info):
    def wrapper_view(context, request):
        if is_cors_request(request):
            maybe_add_cors_to_response_headers(request)
        return view(context, request)
    return wrapper_view
