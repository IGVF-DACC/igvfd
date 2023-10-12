from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config


def includeme(config):
    config.scan(__name__, categories=None)
    config.add_route('verify-email', '/verify-email{slash:/?}')


@view_config(
    route_name='verify-email',
    request_method='GET',
    permission='view',
)
def email_verification(context, request):
    if request.authenticated_userid:
        email = request.GET.get('email')
        try:
            user_to_verify = request.embed(f'/users/{email}', '@@object')
            viewing_groups = user_to_verify.get('viewing_groups', [])
            verified_user = 'IGVF' in viewing_groups
        except KeyError:
            verified_user = False
        return {
            'email': email,
            'verified': verified_user,
            'viewing_groups': viewing_groups,
            'user': user_to_verify
        }
    else:
        raise HTTPForbidden('You are not authorized to perform email address verification.')
