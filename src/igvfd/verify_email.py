from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED

from snovault.interfaces import STORAGE


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
        #session = request.registry[STORAGE].DBSession()
        #statement = select(User).filter_by(email=email)
        email = request.GET.get['email']
        return {'foo': 'bar',
                'user': request.authenticated_userid,
                'email_to_check': email
                }
    else:
        return {'no': 'way'}
