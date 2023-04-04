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
            }
        },
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
            }
        }
    }
