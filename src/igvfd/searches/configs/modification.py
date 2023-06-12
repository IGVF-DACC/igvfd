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
        },
        'facet_groups': [
            {
                'title': 'Modification',
                'facet_fields': [
                    'cas',
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
