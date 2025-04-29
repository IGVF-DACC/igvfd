from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Software'
)
def software():
    return {
        'facets': {
            'used_by': {
                'title': 'Used By'
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
            'publication_identifiers': {
                'title': 'Publication Identifiers'
            },
            'used_by': {
                'title': 'Used by'
            },
            'lab': {
                'title': 'Lab'
            },
            'categories': {
                'title': 'Categories',
            }
        }
    }
