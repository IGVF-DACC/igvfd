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
            'source.title': {
                'title': 'Source'
            },
            'biosample_term.term_name': {
                'title': 'Biosample Term'
            },
            'disease_terms.term_name': {
                'title': 'Disease'
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
                    'biosample_term.term_name',
                    'disease_terms.term_name',
                ]
            },
            {
                'title': 'Provenance',
                'facet_fields': [
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
            'donor': {
                'title': 'Donor'
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
