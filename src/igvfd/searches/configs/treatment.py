from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Treatment'
)
def treatment():
    return {
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
        }
    }
