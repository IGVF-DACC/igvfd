from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Biomarker'
)
def biomarker():
    return {
        'facets': {
            'name': {
                'title': 'Name'
            },
            'quantification': {
                'title': 'Quantification'
            },
            'classification': {
                'title': 'Classification'
            },
            'gene': {
                'title': 'Gene'
            },
        },
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'name': {
                'title': 'Name'
            },
            'quantification': {
                'title': 'Quantification'
            },
            'classification': {
                'title': 'Classification'
            },
            'synonyms': {
                'title': 'Synonyms'
            },
            'gene': {
                'title': 'Gene'
            },
        }
    }
