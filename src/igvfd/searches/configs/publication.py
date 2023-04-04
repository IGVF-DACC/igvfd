from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Publication'
)
def publication():
    return {
        'columns': {
            'title': {
                'title': 'Title'
            },
            'lab': {
                'title': 'Lab'
            },
            'authors': {
                'title': 'Authors'
            },
            'date_published': {
                'title': 'Publication Date'
            },
            'issue': {
                'title': 'Issue'
            },
            'page': {
                'title': 'Page'
            },
            'volume': {
                'title': 'Volume'
            },
            'journal': {
                'title': 'Journal'
            },
            'status': {
                'title': 'Status'
            },
            'identifiers': {
                'title': 'Identifiers'
            },
        }
    }
