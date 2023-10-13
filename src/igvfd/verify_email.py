from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config
from pyramid.security import Allowed
from pyramid.security import Denied


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
        userid = request.unauthenticated_userid
        email = request.GET.get('email')
        try:
            has_view_permission = request.has_permission('view')
            is_allowed = isinstance(has_view_permission, Allowed)
            user_to_verify = request.embed(f'/users/{email}', '@@object', as_user=userid)
            viewing_groups = user_to_verify.get('viewing_groups', [])
            verified_user = 'IGVF' in viewing_groups
        except KeyError:
            verified_user = False
        return {
            'email': email,
            'verified': verified_user,
            'viewing_groups': viewing_groups,
            'has_view_permission': has_view_permission,
            'is_allowed': is_allowed,
        }
    else:
        raise HTTPForbidden('You are not authorized to perform email address verification.')
