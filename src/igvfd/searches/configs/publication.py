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
        },
        'facet_groups': [
            {
                'title': 'Publication',
                'facet_fields': [
                    'published_by',
                ]
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'lab.title',
                    'award.component',
                ]
            },
            {
                'title': 'Quality',
                'facet_fields': [
                    'status',
                ]
            },
        ],
        'columns': {
            'title': {
                'title': 'Title'
            },
            'lab.title': {
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
