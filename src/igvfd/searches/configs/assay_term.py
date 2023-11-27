from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='AssayTerm'
)
def assay_term():
    return {
        'facets': {
            'assay_slims': {
                'title': 'Assay Type',
            },
            'category_slims': {
                'title': 'Assay Category',
            },
            'objective_slims': {
                'title': 'Assay Objective',
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
                'title': 'Assay',
                'facet_fields': [
                    'assay_slims',
                    'category_slims',
                    'objective_slims',
                ],
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
                ],
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
            }
        }
    }
