from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Biosample'
)
def biosample():
    return {
        'facets': {
            'classification': {
                'title': 'Classification',
            },
            'collections': {
                'title': 'Collections',
            },
            'lab.title': {
                'title': 'Lab',
            },
            'award.component': {
                'title': 'Award',
            },
            'status': {
                'title': 'Status'
            },
            'virtual': {
                'title': 'Virtual'
            },
            'type': {
                'title': 'Object Type'
            },
        },
        'facet_groups': [
            {
                'title': 'Sample',
                'facet_fields': [
                    'classification',
                    'virtual',
                ]
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'collections',
                    'lab.title',
                    'award.component',
                    'type',
                ]
            },
            {
                'title': 'Quality',
                'facet_fields': [
                    'status',
                ]
            },
        ],
    }
