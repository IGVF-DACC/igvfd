from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='ReferenceFile'
)
def reference_file():
    return {
        'facets': {
            'file_format': {
                'title': 'File Format'
            },
            'content_type': {
                'title': 'Content Type'
            },
            'assembly': {
                'title': 'Assembly'
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
            }
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
                'title': 'Analysis',
                'facet_fields': [
                    'assembly',
                ],
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'collections',
                    'lab.title',
                    'award.component',
                ],
            },
            {
                'title': 'Quality',
                'facet_fields': [
                    'upload_status',
                    'status',
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
            'assembly': {
                'title': 'Assembly'
            },
            'transcriptome_annotation': {
                'title': 'Transcriptome Annotation'
            },
            'upload_status': {
                'title': 'Upload Status'
            }
        }
    }
