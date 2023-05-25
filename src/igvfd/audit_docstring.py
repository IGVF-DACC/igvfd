from pyramid.view import view_config


def includeme(config):
    config.add_route('audit-docstring', '/audit-docstring{slash:/?}')
    config.scan(__name__)


@view_config(route_name='audit-docstring', request_method='GET')
def audit_docstring(context, request):
    return {'message': 'Audit Docstring'}
