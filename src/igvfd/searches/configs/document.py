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
            'standardized_file_format': {
                'title': 'Standardized File Format'
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
