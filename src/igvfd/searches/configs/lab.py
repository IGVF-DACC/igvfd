from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Lab'
)
def lab():
    return {
        'facets': {
            'awards.component': {
                'title': 'Award'
            },
            'institute_label': {
                'title': 'Institute'
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
            'title': {
                'title': 'Title'
            },
            'aliases': {
                'title': 'Aliases'
            },
            'awards': {
                'title': 'Awards'
            },
            'name': {
                'title': 'Name'
            },
            'status': {
                'title': 'Status'
            },
            'pi': {
                'title': 'Principle Investigator'
            },
            'institute_label': {
                'title': 'Institute Label'
            }
        }
    }
