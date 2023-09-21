from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='MultiplexedSample'
)
def multiplexed_sample():
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
                'title': 'Sources',
            },
            'status': {
                'title': 'Status'
            },
            'biomarkers.classification': {
                'title': 'Biomarkers Classification'
            },
            'virtual': {
                'title': 'Virtual'
            }
        },
        'facet_groups': [
            {
                'title': 'Sample',
                'facet_fields': [
                    'sample_terms.term_name',
                    'disease_terms.term_name',
                    'treatments.treatment_term_name',
                    'biomarkers.classification',
                    'virtual',
                    'classification',
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
                'title': 'Classification',
            },
            'sample_terms': {
                'title': 'Sample Terms'
            },
            'donors': {
                'title': 'Donors'
            },
            'date_obtained': {
                'title': 'Date Obtained'
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
            'summary': {
                'title': 'Summary'
            },
            'virtual': {
                'title': 'Virtual'
            },
            'description': {
                'title': 'Description'
            }
        }
    }
