from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='SoftwareVersion'
)
def software_version():
    return {
        'facets': {
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
            'software.title': {
                'title': 'Title'
            },
            'status': {
                'title': 'Status'
            },
            'version': {
                'title': 'Version'
            },
            'lab': {
                'title': 'Lab'
            },
        }
    }
