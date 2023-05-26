from pyramid.view import view_config


def includeme(config):
    config.add_route('audit_docstring', '/audit-docstring')
    config.scan(__name__)


@view_config(route_name='audit_docstring', request_method='GET')
def audit_docstring(context, request):
    return {'message': 'Audit Docstring'}
