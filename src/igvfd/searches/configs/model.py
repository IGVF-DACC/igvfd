from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Model'
)
def model():
    return {
        'facets': {
            'collections': {
                'title': 'Collections',
            },
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award'
            },
            'status': {
                'title': 'Status'
            },
            'model_type': {
                'title': 'Model Type'
            },
            'prediction_objects': {
                'title': 'Prediction Objects'
            }
        },
        'facet_groups': [
            {
                'title': 'File Set',
                'facet_fields': [
                    'model_type',
                    'prediction_objects',
                ],
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'collections',
                    'lab.title',
                    'award.component',
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
            'accession': {
                'title': 'Accession'
            },
            'alternate_accessions': {
                'title': 'Alternate Accessions'
            },
            'uuid': {
                'title': 'UUID'
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
            'award': {
                'title': 'Award'
            },
            'model_name': {
                'title': 'Model Name'
            },
            'model_type': {
                'title': 'Model Type'
            },
            'prediction_objects': {
                'title': 'Prediction Objects'
            },
            'summary': {
                'title': 'Summary'
            }
        }
    }
