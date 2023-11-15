from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='PrimaryCell'
)
def primary_cell():
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
                'title': 'Sources',
            },
            'status': {
                'title': 'Status'
            },
            'virtual': {
                'title': 'Virtual'
            },
            'biomarkers.classification': {
                'title': 'Biomarkers Classification'
            },
            'type': {
                'title': 'Object Type'
            },
            'audit.ERROR.category': {
                'title': 'Audit Category: Error'
            },
            'audit.NOT_COMPLIANT.category': {
                'title': 'Audit Category: Not Compliant'
            },
            'audit.WARNING.category': {
                'title': 'Audit Category: Warning'
            },
            'audit.INTERNAL_ACTION.category': {
                'title': 'Audit Category: Internal Action'
            },
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
                    'virtual',
                ]
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'collections',
                    'lab.title',
                    'award.component',
                    'sources.title',
                    'type',
                ]
            },
            {
                'title': 'Quality',
                'facet_fields': [
                    'status',
                    'audit.ERROR.category',
                    'audit.NOT_COMPLIANT.category',
                    'audit.WARNING.category',
                    'audit.INTERNAL_ACTION.category',
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
            },
            'alternate_accessions': {
                'title': 'Alternate Accessions'
            },
            'classification': {
                'title': 'Classification'
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
            },
            'description': {
                'title': 'Description'
            }
        }
    }
