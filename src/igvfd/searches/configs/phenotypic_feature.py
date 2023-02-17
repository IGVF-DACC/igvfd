from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='PhenotypicFeature'
)
def phenotypic_feature():
    return {
        'facets': {
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award'
            },
            'status': {
                'title': 'Status'
            }
        },
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
            'lab': {
                'title': 'Lab'
            }
        }
    }
