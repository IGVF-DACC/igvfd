from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Gene'
)
def gene():
    return {
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'title': {
                'title': 'Title'
            },
            'geneid': {
                'title': 'NCBI Entrez GeneID'
            },
            'symbol': {
                'title': 'Gene symbol'
            },
            'synonyms': {
                'title': 'Synonyms'
            },
            'dbxrefs': {
                'title': 'External resources'
            },
            'status': {
                'title': 'Status'
            },
        }
    }
