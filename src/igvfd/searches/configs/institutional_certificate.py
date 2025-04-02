from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='InstitutionalCertificate'
)
def institutional_certificate():
    return {
        'facets': {
            'data_use_limitation_summary': {
                'title': 'Data Use Limitation',
            },
            'controlled_access': {
                'title': 'Controlled Access',
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
            'certificate_identifier': {
                'title': 'Certificate Identifier'
            },
            'data_use_limitation_summary': {
                'title': 'Data Use Limitation'
            },
            'urls': {
                'title': 'URL'
            },
            'uuid': {
                'title': 'UUID'
            },
            'aliases': {
                'title': 'Aliases'
            },
            'status': {
                'title': 'Status'
            },
            'lab': {
                'title': 'Lab'
            },
            'award': {
                'title': 'Award'
            },
            'summary': {
                'title': 'Summary'
            },
            'controlled_access': {
                'title': 'Controlled Access',
            }
        }
    }
