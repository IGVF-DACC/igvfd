from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='User'
)
def user():
    return {
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'title': {
                'title': 'Title'
            },
            'lab': {
                'title': 'Lab'
            },
            'status': {
                'title': 'Status'
            },
        }
    }
