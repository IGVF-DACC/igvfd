from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Sample'
)
def sample():
    return {
        'facets': {
            'classifications': {
                'title': 'Classifications',
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
            'status': {
                'title': 'Status'
            },
            'virtual': {
                'title': 'Virtual'
            },
            'file_sets.assay_term.term_name': {
                'title': 'Assay'
            },
            'sample_terms': {
                'title': 'Sample Terms'
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
            'treatments.term_name': {
                'title': 'Treatment term name'
            },
            'treatments.type': {
                'title': 'Treatment type'
            },
            'treatments.purpose': {
                'title': 'Treatment purpose'
            },
        },
        'facet_groups': [
            {
                'title': 'Sample',
                'facet_fields': [
                    'classifications',
                    'sample_terms',
                    'virtual',
                    'file_sets.assay_term.term_name',
                ]
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'collections',
                    'lab.title',
                    'award.component',
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
            {
                'title': 'Treatments',
                'facet_fields': [
                    'treatments.Purpose',
                    'treatments.treatment_type',
                    'treatments.term_name',
                ]
            },
        ],
    }
