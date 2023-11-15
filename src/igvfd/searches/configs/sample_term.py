from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='SampleTerm'
)
def sample_term():
    return {
        'facets': {
            'organ_slims': {
                'title': 'Organ',
            },
            'cell_slims': {
                'title': 'Cell',
            },
            'developmental_slims': {
                'title': 'Developmental Slims',
            },
            'system_slims': {
                'title': 'System Slims',
            },
            'status': {
                'title': 'Status'
            },
            'ontology': {
                'title': 'Ontology'
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
                    'organ_slims',
                    'cell_slims',
                    'developmental_slims',
                    'system_slims',
                ]
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'type',
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
                ]
            },
        ],
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'term_id': {
                'title': 'Term ID'
            },
            'term_name': {
                'title': 'Term Name'
            },
            'synonyms': {
                'title': 'Synonyms'
            },
            'status': {
                'title': 'Status'
            },
            'submitted_by': {
                'title': 'Submitted By'
            },
        }
    }
