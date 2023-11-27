from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Document'
)
def document():
    return {
        'facets': {
            'document_type': {
                'title': 'Document Type'
            },
            'characterization_method': {
                'title': 'Characterization Method'
            },
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award',
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
                'title': 'Document',
                'facet_fields': [
                    'document_type',
                    'characterization_method',
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
            'description': {
                'title': 'Description'
            },
            'aliases': {
                'title': 'Aliases'
            },
            'award': {
                'title': 'Award'
            },
            'document_type': {
                'title': 'Document Type'
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
            'attachment': {
                'title': 'Attachment'
            },
        }
    }
