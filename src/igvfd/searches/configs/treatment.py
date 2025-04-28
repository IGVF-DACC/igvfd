from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Treatment'
)
def treatment():
    return {
        'facets': {
            'purpose': {
                'title': 'Purpose'
            },
            'treatment_type': {
                'title': 'Treatment Type'
            },
            'sources.title': {
                'title': 'Sources'
            },
            'status': {
                'title': 'Status'
            },
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award'
            },
            'depletion': {
                'title': 'Depletion'
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
            'treatment_term_name': {
                'title': 'Treatment Term Name'
            },
            'treatment_type': {
                'title': 'Treatment Type'
            },
            'treatment_term_id': {
                'title': 'Treatment Term ID'
            },
            'purpose': {
                'title': 'Purpose'
            },
            'status': {
                'title': 'Status'
            },
            'amount': {
                'title': 'Amount'
            },
            'amount_units': {
                'title': 'Amount Units'
            },
            'duration': {
                'title': 'Duration'
            },
            'duration_units': {
                'title': 'Duration Units'
            },
            'summary': {
                'title': 'Summary'
            },
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award'
            },
            'depletion': {
                'title': 'Depletion'
            }
        }
    }
