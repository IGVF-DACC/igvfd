from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='PhenotypicFeature'
)
def phenotypic_feature():
    return {
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'feature': {
                'title': 'Phenotypic feature'
            },
            'status': {
                'title': 'Status'
            },
        }
    }
