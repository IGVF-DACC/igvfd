from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='HumanGenomicVariant'
)
def human_genomic_variant():
    return {
        'facets': {
            'assembly': {
                'title': 'Genome Assembly'
            },
            'status': {
                'title': 'Status'
            },
        },
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'status': {
                'title': 'Status'
            },
            'ref': {
                'title': 'Reference Allele'
            },
            'alt': {
                'title': 'Alternative Allele'
            },
            'assembly': {
                'title': 'Genome Assembly'
            },
            'position': {
                'title': 'Position'
            },
            'refseq_id': {
                'title': 'RefSeq Sequence Identifier'
            },
            'reference_sequence': {
                'title': 'Reference Sequence'
            },
            'chromosome': {
                'title': 'Chromosome'
            },
            'rsid': {
                'title': 'RS Identifier'
            },
            'aliases': {
                'title': 'Aliases'
            }
        }
    }
