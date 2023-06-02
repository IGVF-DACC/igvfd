from pyramid.view import view_config


def includeme(config):
    config.scan(__name__)
    config.add_route('audit-docstring', '/audit-docstring')


@view_config(route_name='audit-docstring', request_method='GET')
def audit_docstring(context, request):
    return {'message': 'Audit Docstring'}
