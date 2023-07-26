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
            'status': {
                'title': 'Status'
            }
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
            'status': {
                'title': 'Status'
            },
            'gene': {
                'title': 'Gene'
            },
            'lab': {
                'title': 'Lab'
            }
        }
    }
