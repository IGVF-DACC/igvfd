from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='OpenReadingFrame'
)
def open_reading_frame():
    return {
        'facets': {
            'status': {
                'title': 'Status'
            }
        },
        'columns': {
            'ord_id': {
                'title': 'ORF ID'
            },
            'gene': {
                'title': 'ENSEMBL GeneID'
            },
            'protein_id': {
                'title': 'ENSEMBL ProteinID'
            },
            'dbxrefs': {
                'title': 'External resources'
            },
            'status': {
                'title': 'Status'
            },
        }
    }
