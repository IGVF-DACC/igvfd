from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='AlignmentFile'
)
def alignment_file():
    return {
        'facets': {
            'file_format': {
                'title': 'File Format'
            },
            'content_type': {
                'title': 'Content Type'
            },
            'collections': {
                'title': 'Collections'
            },
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award',
            },
            'upload_status': {
                'title': 'Upload Status'
            },
            'status': {
                'title': 'Status'
            },
            'audit.ERROR.category': {
                'title': 'Error Audits'
            },
            'audit.NOT_COMPLIANT.category': {
                'title': 'Not Compliant Audits'
            },
            'audit.WARNING.category': {
                'title': 'Warning Audits'
            },
            'audit.INTERNAL_ACTION.category': {
                'title': 'Internal Action Audits'
            },
        },
        'facet_groups': [
            {
                'title': 'Format',
                'facet_fields': [
                    'file_format',
                    'content_type',
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
                    'audit.INTERNAL_ACTION.category'
                ],
            },
        ],
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'accession': {
                'title': 'Accession'
            },
            'alternate_accessions': {
                'title': 'Alternate Accessions'
            },
            'content_type': {
                'title': 'Content Type'
            },
            'file_format': {
                'title': 'File Format'
            },
            'lab': {
                'title': 'Lab'
            },
            'status': {
                'title': 'Status'
            },
            'file_set': {
                'title': 'File Set'
            },
            'reference_files': {
                'title': 'Reference Files'
            },
            'content_summary': {
                'title': 'Content Summary'
            },
            'upload_status': {
                'title': 'Upload Status'
            }
        }
    }
