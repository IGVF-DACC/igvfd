from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED


def includeme(config):
    config.scan(__name__, categories=None)
    config.add_route('verify-email', '/verify-email{slash:/?}')


@view_config(
    route_name='verify-email',
    request_method='GET',
    permission=NO_PERMISSION_REQUIRED,
)
def email_verification(context, request):
    if request.authenticated_userid:
        return {'foo': 'bar',
                'user': request.authenticated_userid
                }
    else:
        return {'no': 'way'}
