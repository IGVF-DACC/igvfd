from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Source'
)
def source():
    return {
        'facets': {
            'status': {
                'title': 'Status'
            },
        },
        'columns': {
            'title': {
                'title': 'Title'
            },
            'description': {
                'title': 'Description',
            },
            'status': {
                'title': 'Status'
            },
        }
    }
