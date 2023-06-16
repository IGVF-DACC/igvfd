from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='PredictionSet'
)
def cell_line():
    return {
        'facets': {
            'status': {
                'title': 'Status'
            },
            'award.component': {
                'title': 'Award'
            },
            'lab.title': {
                'title': 'Lab'
            },
            'prediction_type': {
                'title': 'Prediction Type'
            }
        },
        'columns': {
            'accession': {
                'title': 'Accession'
            },
            'aliases': {
                'title': 'Aliases'
            },
            'status': {
                'title': 'Status'
            },
            'lab': {
                'title': 'Lab'
            },
            'prediction_type': {
                'title': 'Prediction Type'
            },
            'samples': {
                'title': 'Samples'
            },
            'donors': {
                'title': 'Donors'
            },
        }

    }
