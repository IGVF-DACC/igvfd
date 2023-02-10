from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Document'
)
def document():
    return {
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
