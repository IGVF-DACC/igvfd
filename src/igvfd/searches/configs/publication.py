from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Publication'
)
def publication():
    return {
        'facets': {
            'published_by': {
                'title': 'Published By'
            },
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award'
            },
            'status': {
                'title': 'Status'
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
            'publication_identifiers': {
                'title': 'Publication Identifiers'
            }
        }
    }
