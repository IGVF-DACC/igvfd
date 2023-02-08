from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Software'
)
def software():
    return {
        'facets': {
            'used_by': {
                'title': 'Used by'
            },
            'award.component': {
                'title': 'Award'
            },
            'lab.title': {
                'title': 'Lab'
            },
        },
        'columns': {
            'title': {
                'title': 'Title'
            },
            'name': {
                'title': 'Name'
            },
            'status': {
                'title': 'Status'
            },
            'description': {
                'title': 'Description'
            },
            'source_url': {
                'title': 'Source URL'
            },
            'references': {
                'title': 'References'
            },
            'used_by': {
                'title': 'Used by'
            },
        }
    }
