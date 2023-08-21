from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='OntologyTerm'
)
def ontology_term():
    return {
        'facets': {
            'ontology': {
                'title': 'Ontology'
            },
            'status': {
                'title': 'Status'
            },
            'type': {
                'title': 'Object Type',
            },
        },
        'facet_groups': [
            {
                'title': 'Assay',
                'facet_fields': [
                    'assay_slims',
                    'category_slims',
                    'objective_slims',
                ]
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'type',
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
            }
        }
    }
