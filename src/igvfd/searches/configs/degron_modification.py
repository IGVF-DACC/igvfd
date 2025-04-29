from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='DegronModification'
)
def degron_modification():
    return {
        'facets': {
            'degron_system': {
                'title': 'Degron System'
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
            'degron_system': {
                'title': 'Degron System'
            },
            'tagged_proteins': {
                'title': 'Tagged Proteins'
            },
            'product_id': {
                'title': 'Product ID'
            },
            'lab': {
                'title': 'Lab'
            }
        }
    }
