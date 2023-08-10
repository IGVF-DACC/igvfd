from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='InVitroSystem'
)
def in_vitro_system():
    return {
        'facets': {
            'sample_terms.term_name': {
                'title': 'Sample Terms',
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
            'sources.title': {
                'title': 'Source',
            },
            'status': {
                'title': 'Status'
            },
            'virtual': {
                'title': 'Virtual'
            },
            'biomarkers.classification': {
                'titlle': 'Biomarkers Classification'
            }
        },
        'facet_groups': [
            {
                'title': 'Sample',
                'facet_fields': [
                    'sample_terms.term_name',
                    'disease_terms.term_name',
                    'treatments.treatment_term_name',
                    'taxa',
                    'sex',
                    'classification',
                    'biomarkers.classification',
                ]
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'collections',
                    'lab.title',
                    'award.component',
                    'sources.title',
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
            'alternate_accessions': {
                'title': 'Alternate Accessions'
            },
            'classification': {
                'title': 'Classification'
            },
            'sample_terms': {
                'title': 'Sample Terms'
            },
            'donors': {
                'title': 'Donors'
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
