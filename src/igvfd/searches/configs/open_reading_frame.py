from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='OpenReadingFrame'
)
def open_reading_frame():
    return {
        'facets': {
            'gene': {
                'title': 'Gene'
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
