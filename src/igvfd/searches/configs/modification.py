from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Modification'
)
def modification():
    return {
        'facets': {
            'cas': {
                'title': 'Cas'
            },
            'modality': {
                'title': 'Modality'
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
            'cas_species': {
                'title': 'Cas Species'
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
                'title': 'Modification',
                'facet_fields': [
                    'cas',
                    'cas_species',
                    'modality',
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
                    'audit.ERROR.category',
                    'audit.NOT_COMPLIANT.category',
                    'audit.WARNING.category',
                    'audit.INTERNAL_ACTION.category',
                ]
            },
        ],
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'summary': {
                'title': 'Summary'
            },
            'cas': {
                'title': 'Cas'
            },
            'modality': {
                'title': 'Modality'
            },
            'fused_domain': {
                'title': 'Fused Domain'
            },
            'tagged_protein': {
                'title': 'Tagged Protein'
            },
            'product_id': {
                'title': 'Product ID'
            },
            'lab': {
                'title': 'Lab'
            },
            'cas_species': {
                'title': 'Cas Species'
            }
        }
    }
