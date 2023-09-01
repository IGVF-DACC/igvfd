from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='MatrixFile'
)
def matrix_file():
    return {
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
            'upload_status': {
                'title': 'Upload Status'
            }
        }
    }
