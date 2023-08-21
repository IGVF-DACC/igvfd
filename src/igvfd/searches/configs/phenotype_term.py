from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='PhenotypeTerm'
)
def phenotype_term():
    return {
        'facets': {
            'ontology': {
                'title': 'Ontology'
            },
            'status': {
                'title': 'Status'
            },
            'term_id': {
                'title': 'Term ID'
            },
            'term_name': {
                'title': 'Term Name'
            },
        },
        'facet_groups': [
            {
                'title': 'Phenotype',
                'facet_fields': [
                    'term_id',
                    'term_name',
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
