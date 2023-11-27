from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Biomarker'
)
def biomarker():
    return {
        'facets': {
            'name': {
                'title': 'Name'
            },
            'quantification': {
                'title': 'Quantification'
            },
            'classification': {
                'title': 'Classification'
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
                'title': 'Biomarker',
                'facet_fields': [
                    'name',
                    'quantification',
                    'classification',
                ]
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'lab.title',
                    'award.component',
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
            'name': {
                'title': 'Name'
            },
            'quantification': {
                'title': 'Quantification'
            },
            'classification': {
                'title': 'Classification'
            },
            'synonyms': {
                'title': 'Synonyms'
            },
            'status': {
                'title': 'Status'
            },
            'gene': {
                'title': 'Gene'
            },
            'lab': {
                'title': 'Lab'
            }
        }
    }
