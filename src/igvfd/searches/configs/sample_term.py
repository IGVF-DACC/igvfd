from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='SampleTerm'
)
def sample_term():
    return {
        'facets': {
            'organ_slims': {
                'title': 'Organ',
            },
            'cell_slims': {
                'title': 'Cell',
            },
            'developmental_slims': {
                'title': 'Developmental Slims',
            },
            'system_slims': {
                'title': 'System Slims',
            },
            'status': {
                'title': 'Status'
            },
        },
        'facet_groups': [
            {
                'title': 'Sample',
                'facet_fields': [
                    'organ_slims',
                    'cell_slims',
                    'developmental_slims',
                    'system_slims',
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
            'term_id': {
                'title': 'Term ID'
            },
            'term_name': {
                'title': 'Term Name'
            },
            'synonyms': {
                'title': 'Synonyms'
            },
            'status': {
                'title': 'Status'
            },
            'submitted_by': {
                'title': 'Submitted By'
            },
        }
    }
