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
            'references': {
                'title': 'References'
            },
            'used_by': {
                'title': 'Used by'
            },
            'lab.title': {
                'title': 'Lab'
            },
        }
    }
