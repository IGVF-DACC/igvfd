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
            'source.title': {
                'title': 'Source'
            },
            'status': {
                'title': 'Status'
            }
        },
        'facet_groups': [
            {
                'title': 'Treatment',
                'facet_fields': [
                    'purpose',
                    'treatment_type',
                ],
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'source.title',
                ],
            },
            {
                'title': 'Quality',
                'facet_fields': [
                    'status',
                ],
            }
        ],
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
        }
    }
