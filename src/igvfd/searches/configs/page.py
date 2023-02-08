from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Page'
)
def page():
    return {
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'name': {
                'title': 'Name'
            },
            'title': {
                'title': 'Title'
            },
            'parent': {
                'title': 'Parent'
            },
            'lab': {
                'title': 'Lab'
            },
            'status': {
                'title': 'Status'
            },
        }
    }
