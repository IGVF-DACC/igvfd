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
        'facet_groups': [
            {
                'title': 'Software',
                'facet_fields': [
                    'used_by',
                ],
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'lab.title',
                    'award.component',
                ],
            },
            {
                'title': 'Quality',
                'facet_fields': [
                    'status',
                    'audit.ERROR.category',
                    'audit.NOT_COMPLIANT.category',
                    'audit.WARNING.category',
                    'audit.INTERNAL_ACTION.category',
                ],
            },
        ],
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
        }
    }
