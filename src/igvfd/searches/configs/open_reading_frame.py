from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='OpenReadingFrame'
)
def open_reading_frame():
    return {
        'facets': {
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award'
            },
            'status': {
                'title': 'Status'
            }
        },
        'columns': {
            'orf_id': {
                'title': 'ORF ID'
            },
            'genes': {
                'title': 'ENSEMBL GeneIDs'
            },
            'protein_id': {
                'title': 'ENSEMBL ProteinID'
            },
            'dbxrefs': {
                'title': 'External resources'
            },
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award'
            },
            'status': {
                'title': 'Status'
            },
        }
    }
