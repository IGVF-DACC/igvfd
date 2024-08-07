from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='AuxiliarySet'
)
def auxiliary_set():
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
            'file_set_type': {
                'title': 'File Set Type'
            },
            'donors.taxa': {
                'title': 'Taxa'
            },
            'samples.classifications': {
                'title': 'Classifications',
            },
            'samples.sample_terms.term_name': {
                'title': 'Sample Term',
            },
            'samples.targeted_sample_term.term_name': {
                'title': 'Targeted Sample Term',
            },
            'samples.disease_terms.term_name': {
                'title': 'Disease Term',
            },
            'measurement_sets.preferred_assay_title': {
                'title': 'Auxiliary Data Of',
            },
            'collections': {
                'title': 'Collections',
            },
            'files.content_type': {
                'title': 'Available File Types',
            },
            'file_set_type': {
                'title': 'File Set Type',
            },
            'type': {
                'title': 'Object Type',
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
                    'donors.taxa',
                    'samples.classifications',
                    'samples.sample_terms.term_name',
                    'samples.targeted_sample_term.term_name',
                    'samples.disease_terms.term_name',
                ],
            },
            {
                'title': 'File Set',
                'facet_fields': [
                    'file_set_type',
                    'measurement_sets.preferred_assay_title',
                ],
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'collections',
                    'lab.title',
                    'award.component',
                    'type',
                ],
            },
            {
                'title': 'File Data',
                'facet_fields': [
                    'files.content_type'
                ],
            },
            {
                'title': 'Quality',
                'facet_fields': [
                    'status',
                    'audit.ERROR.category',
                    'audit.NOT_COMPLIANT.category',
                    'audit.WARNING.category',
                    'audit.INTERNAL_ACTION.category',
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
            'file_set_type': {
                'title': 'File Set Type'
            },
            'samples': {
                'title': 'Samples'
            },
            'donors': {
                'title': 'Donors'
            },
            'summary': {
                'title': 'Summary'
            },
            'measurement_sets': {
                'title': 'Measurement Sets'
            }
        }
    }
