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
            'sample_terms.term_name': {
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
            'treatments.purpose': {
                'title': 'Treatment Purpose'
            },
            'treatments.treatment_type': {
                'title': 'Treatment Type'
            },
            'treatments.treatment_term_name': {
                'title': 'Treatment Term Name'
            },
            'modifications.type': {
                'title': 'Type'
            },
            'modifications.cas': {
                'title': 'Cas'
            },
            'modifications.fused_domain': {
                'title': 'Fused domain'
            },
            'modifications.modality': {
                'title': 'Modality'
            },
            'modifications.tagged_proteins.symbol': {
                'title': 'Tagged proteins'
            },
        },
        'facet_groups': [
            {
                'title': 'Sample',
                'facet_fields': [
                    'classifications',
                    'sample_terms.term_name',
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
                    'treatments.purpose',
                    'treatments.treatment_type',
                    'treatments.treatment_term_name',
                ]
            },
            {
                'title': 'Modifications',
                'facet_fields': [
                    'modifications.@type',
                    'modifications.cas',
                    'modifications.modality',
                    'modifications.fused_domain',
                    'modifications.tagged_proteins.symbol',
                ]
            },
        ],
    }
