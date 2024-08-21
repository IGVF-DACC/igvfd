from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='File'
)
def file():
    return {
        'facets': {
            'award.component': {
                'title': 'Award',
            },
            'collections': {
                'title': 'Collections'
            },
            'content_type': {
                'title': 'Content Type'
            },
            'file_format': {
                'title': 'File Format'
            },
            'file_format_type': {
                'title': 'File Format Type'
            },
            'assembly': {
                'title': 'Assembly'
            },
            'transcriptome_annotation': {
                'title': 'Transcriptome Annotation'
            },
            'cell_type_annotation.term_name': {
                'title': 'Cell Type Annotation'
            },
            'lab.title': {
                'title': 'Lab'
            },
            'status': {
                'title': 'Status'
            },
            'upload_status': {
                'title': 'Upload Status'
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
                'title': 'Format',
                'facet_fields': [
                    'file_format',
                    'file_format_type',
                    'content_type',
                    'cell_type_annotation.term_name',
                ],
            },
            {
                'title': 'Assembly',
                'facet_fields': [
                    'assembly',
                    'transcriptome_annotation',
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
                'title': 'Quality',
                'facet_fields': [
                    'upload_status',
                    'status',
                    'audit.ERROR.category',
                    'audit.NOT_COMPLIANT.category',
                    'audit.WARNING.category',
                    'audit.INTERNAL_ACTION.category',
                ],
            },
        ]
    }
