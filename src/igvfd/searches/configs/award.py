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
            }
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
            'status': {
                'title': 'Status'
            }
        }
    }
