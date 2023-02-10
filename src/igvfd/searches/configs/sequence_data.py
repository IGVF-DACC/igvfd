from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='SequenceData'
)
def sequence_data():
    return {
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'accession': {
                'title': 'Accession'
            },
            'content_type': {
                'title': 'Content Type'
            },
            'file_format': {
                'title': 'File Format'
            },
        }
    }
