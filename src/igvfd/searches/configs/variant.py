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
                    'audit.ERROR.category',
                    'audit.NOT_COMPLIANT.category',
                    'audit.WARNING.category',
                    'audit.INTERNAL_ACTION.category',
                ],
            },
        ],
    }
