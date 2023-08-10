from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='WholeOrganism'
)
def whole_organism():
    return {
        'facets': {
            'taxa': {
                'title': 'Taxa'
            },
            'sex': {
                'title': 'Sex'
            },
            'treatments.treatment_type': {
                'title': 'Treatments'
            },
            'biomarkers.classification': {
                'title': 'Biomarkers'
            },
            'sources.title': {
                'title': 'Sources'
            },
            'sample_terms.term_name': {
                'title': 'Sample Terms'
            },
            'disease_terms.term_name': {
                'title': 'Disease Terms'
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
            'virtual': {
                'title': 'Virtual'
            }
        },
        'facet_groups': [
            {
                'title': 'Sample',
                'facet_fields': [
                    'taxa',
                    'sex',
                    'treatments.treatment_type',
                    'biomarkers.classification',
                    'sample_terms.term_name',
                    'disease_terms.term_name',
                    'virtual',
                ]
            },
            {
                'title': 'Provenance',
                'facet_fields': [
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
            'sample_terms': {
                'title': 'Sample Terms'
            }
            'alternate_accessions': {
                'title': 'Alternate Accessions'
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
            'summary': {
                'title': 'Summary'
            },
            'virtual': {
                'title': 'Virtual'
            }
        }
    }
