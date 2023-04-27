from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='PlatformTerm'
)
def platform_term():
    return {
        'facets': {
            'status': {
                'title': 'Status'
            },
        },
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
