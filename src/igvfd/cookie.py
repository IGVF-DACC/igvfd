import hashlib

from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED


def includeme(config):
    config.scan(__name__)
    config.add_route('session-cookie-name', '/session-cookie-name{slash:/?}')


def generate_hash(byte_value):
    return hashlib.sha256(byte_value).hexdigest()


def get_last_six_bytes_of_secret(secret):
    if isinstance(secret, str):
        return secret.encode('utf-8')[-6:]
    return secret[-6:]


def generate_cookie_name(secret):
    # We generate hash using last six bytes of session secret
    # so this value persists across requests. Since it's only
    # a small part of the session secret it doesn't necessary need
    # to be private, but we hash it again for further obfuscation.
    last_six_bytes_of_secret = get_last_six_bytes_of_secret(
        secret
    )
    # We only need first ten characters of hexdigest to create
    # unique identifier.
    hexdigest = generate_hash(
        last_six_bytes_of_secret
    )[:10]
    return f'session-{hexdigest}'


def add_session_cookie_name_to_settings(settings, secret):
    session_cookie_name = generate_cookie_name(secret)
    settings['session_cookie_name'] = session_cookie_name


@view_config(
    route_name='session-cookie-name',
    request_method='GET',
    permission=NO_PERMISSION_REQUIRED,

)
def session_cookie_name(context, request):
    return request.registry.settings.get('session_cookie_name')
