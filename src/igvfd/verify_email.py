from pyramid.httpexceptions import HTTPForbidden
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
        email = request.GET.get('email')
        user_to_verify = request.embed(f'/users/{email}')
        viewing_groups = user_to_verify.get('viewing_groups', [])
        verified_user = 'IGVF' in viewing_groups
        return {
            'email': email,
            'verified': verified_user,
        }
    else:
        raise HTTPForbidden('You are not authorized to perform email address verification.')
