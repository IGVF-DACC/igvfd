from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Tissue'
)
def tissue():
    return {
        'facets': {
            'biosample_term.term_name': {
                'title': 'Biosample Term',
            },
            'disease_terms.term_name': {
                'title': 'Disease Terms',
            },
            'treatments.treatment_term_name': {
                'title': 'Treatments',
            },
            'taxa': {
                'title': 'Taxa',
            },
            'sex': {
                'title': 'Sex'
            },
            'collections': {
                'title': 'Collections',
            },
            'lab.title': {
                'title': 'Lab',
            },
            'award.component': {
                'title': 'Award',
            },
            'source.title': {
                'title': 'Source',
            },
            'status': {
                'title': 'Status'
            },
            'virtual': {
                'title': 'Virtual'
            }
        },
        'facet_groups': [
            {
                'title': 'Sample',
                'facet_fields': [
                    'biosample_term.term_name',
                    'disease_terms.term_name',
                    'treatments.treatment_term_name',
                    'taxa',
                    'sex',
                ]
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'collections',
                    'lab.title',
                    'award.component',
                    'source.title',
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
            'accession': {
                'title': 'Accession'
            },
            'biosample_term': {
                'title': 'Biosample Term'
            },
            'donors': {
                'title': 'Donors'
            },
            'date_obtained': {
                'title': 'Date Obtained'
            },
            'taxa': {
                'title': 'Taxa'
            },
            'award': {
                'title': 'Award'
            },
            'lab': {
                'title': 'Lab'
            },
            'status': {
                'title': 'Status'
            },
            'submitted_by': {
                'title': 'Submitted By'
            },
            'summary': {
                'title': 'Summary'
            },
            'virtual': {
                'title': 'Virtual'
            }
        }
    }
