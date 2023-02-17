from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='InVitroSystem'
)
def in_vitro_system():
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
            'classification': {
                'title': 'Classification',
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
                    'classification',
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
            'classification': {
                'title': 'Classification'
            },
            'biosample_term.term_name': {
                'title': 'Biosample Term'
            },
            'donors.taxa': {
                'title': 'Donor Taxa',
            },
            'donors.sex': {
                'title': 'Donor Sex',
            },
            'originated_from': {
                'title': 'Originated From'
            },
            'taxa': {
                'title': 'Taxa'
            },
            'award': {
                'title': 'Award'
            },
            'lab.title': {
                'title': 'Lab'
            },
            'status': {
                'title': 'Status'
            },
            'submitted_by': {
                'title': 'Submitted By'
            },
        }
    }
