from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='CrisprModification'
)
def crispr_modification():
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
            'tagged_proteins': {
                'title': 'Tagged Proteins'
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
