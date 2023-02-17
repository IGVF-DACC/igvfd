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
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award'
            },
        },
        'facet_groups': [
            {
                'title': 'Biomarker',
                'facet_fields': [
                    'name',
                    'quantification',
                    'classification',
                ]
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'lab.title',
                    'award.component',
                ]
            },
        ],
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
            'lab': {
                'title': 'Lab'
            },
            'award': {
                'title': 'award'
            }
        }
    }
