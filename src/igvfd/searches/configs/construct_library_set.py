from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='ConstructLibrarySet'
)
def construct_library_set():
    return {
        'facets': {
            'award.component': {
                'title': 'Award'
            },
            'lab.title': {
                'title': 'Lab'
            },
            'file_set_type': {
                'title': 'File Set Type'
            },
            'scope': {
                'title': 'Scope'
            },
            'selection_criteria': {
                'title': 'Selection Criteria'
            },
            'collections': {
                'title': 'Collections',
            },
            'status': {
                'title': 'Status'
            },
            'type': {
                'title': 'Object Type',
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
        'facet_groups': [
            {
                'title': 'File Set',
                'facet_fields': [
                    'file_set_type',
                    'selection_criteria',
                    'scope',
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
                    'status',
                    'audit.ERROR.category',
                    'audit.NOT_COMPLIANT.category',
                    'audit.WARNING.category',
                    'audit.INTERNAL_ACTION.category',
                ],
            },
        ],
        'columns': {
            'accession': {
                'title': 'Accession'
            },
            'aliases': {
                'title': 'Aliases'
            },
            'status': {
                'title': 'Status'
            },
            'lab': {
                'title': 'Lab'
            },
            'file_set_type': {
                'title': 'File Set Type'
            },
            'scope': {
                'title': 'Scope'
            },
            'selection_criteria': {
                'title': 'Selection Criteria'
            },
            'genes.symbol': {
                'title': 'Genes'
            },
            'loci': {
                'title': 'Loci'
            },
            'associated_phenotypes.term_name': {
                'title': 'Associated Phenotypes'
            },
            'alternate_accessions': {
                'title': 'Alternate Accessions'
            },
            'summary': {
                'title': 'Summary'
            },
        }
    }
