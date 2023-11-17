from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Gene'
)
def gene():
    return {
        'facets': {
            'taxa': {
                'title': 'Taxa'
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
