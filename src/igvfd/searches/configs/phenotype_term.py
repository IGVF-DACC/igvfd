from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='PhenotypeTerm'
)
def phenotype_term():
    return {
        'facets': {
            'status': {
                'title': 'Status'
            },
            'ontology': {
                'title': 'Ontology'
            }
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
            }
        }
    }
