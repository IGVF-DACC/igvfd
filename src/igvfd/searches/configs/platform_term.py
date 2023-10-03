from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='PlatformTerm'
)
def platform_term():
    return {
        'facets': {
            'ontology': {
                'title': 'Ontology'
            },
            'status': {
                'title': 'Status'
            },
            'company': {
                'title': 'Company'
            },
            'type': {
                'title': 'Object Type',
            },
        },
        'facet_groups': [
            {
                'title': 'Platform',
                'facet_fields': [
                    'company'
                ],
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'type',
                ],
            },
            {
                'title': 'Quality',
                'facet_fields': [
                    'status',
                ],
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
            }
        }
    }
