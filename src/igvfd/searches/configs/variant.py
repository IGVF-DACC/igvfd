from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Variant'
)
def variant():
    return {
        'facets': {
            'alt': {
                'title': 'Alternative Allele',
            },
            'assembly': {
                'title': 'Genome Assembly'
            },
            'ref': {
                'title': 'Reference Allele',
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
                'title': 'Variant',
                'facet_fields': [
                    'assembly',
                    'alt',
                    'ref',
                ],
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'type',
                ],
            },
            {
                'title': 'Quality',
                'facet_fields': [
                    'status',
                ],
            },
        ],
    }
