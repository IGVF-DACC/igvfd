from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config


def includeme(config):
    config.scan(__name__, categories=None)
    config.add_route('verify-igvf-email', '/verify-igvf-email{slash:/?}')


@view_config(
    route_name='verify-igvf-email',
    request_method='GET',
    permission='view',
)
def igvf_email_verification(context, request):
    if request.authenticated_userid:
        email = request.GET.get('email')
        try:
            user = request.embed(f'/users/{email}', as_user=True)
            viewing_groups = user.get('viewing_groups', [])
            is_igvf_viewer = 'IGVF' in viewing_groups
        except KeyError:
            is_igvf_viewer = False
        return {
            'email': email,
            'verified': is_igvf_viewer,
        }
    else:
        raise HTTPForbidden('You are not authorized to perform email address verification.')
