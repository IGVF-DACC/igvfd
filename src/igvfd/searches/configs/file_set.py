from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='FileSet'
)
def file_set():
    return {
        'facets': {
            'collections': {
                'title': 'Collections',
            },
            'donors.taxa': {
                'title': 'Taxa',
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
            'type': {
                'title': 'Object Type',
            },
        },
        'facet_groups': [
            {
                'title': 'File Set',
                'facet_fields': [
                    'donors.taxa',
                    'type',
                ],
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'collections',
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
        ]
    }
