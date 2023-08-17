from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Prediction'
)
def prediction():
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
            },
            'collections': {
                'title': 'Collections',
            },
            'donors.taxa': {
                'title': 'Taxa',
            }
        },
        'facet_groups': [
            {
                'title': 'File Set',
                'facet_fields': [
                    'donors.taxa',
                    'prediction_type',
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
            }
        }
    }
