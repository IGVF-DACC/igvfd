from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Award'
)
def award():
    return {
        'facets': {
            'project': {
                'title': 'Project'
            },
            'status': {
                'title': 'Status'
            },
            'component': {
                'title': 'Component'
            },
            'audit.ERROR.category': {
                'title': 'Audit Category: Error'
            },
            'audit.NOT_COMPLIANT.category': {
                'title': 'Audit Category: Not Compliant'
            },
            'audit.WARNING.category': {
                'title': 'Audit Category: Warning'
            },
            'audit.INTERNAL_ACTION.category': {
                'title': 'Audit Category: Internal Action'
            },
        },
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'title': {
                'title': 'Title'
            },
            'name': {
                'title': 'Name'
            },
            'project': {
                'title': 'Project'
            },
            'component': {
                'title': 'Component'
            },
            'contact_pi': {
                'title': 'Contact P.I.'
            },
            'status': {
                'title': 'Status'
            }
        }
    }
