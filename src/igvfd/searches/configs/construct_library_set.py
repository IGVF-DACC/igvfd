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
            'small_scale_gene_list.symbol': {
                'title': 'Targeted Genes'
            },
            'orf_list.gene.symbol': {
                'title': 'Open Reading Frame Gene'
            },
            'associated_phenotypes.term_name': {
                'title': 'Associated Phenotypes'
            },
            'tiling_modality': {
                'title': 'CRISPR Tiling Modality'
            },
            'guide_type': {
                'title': 'CRISPR Guide Type'
            },
            'applied_to_samples.donors.taxa': {
                'title': 'Taxa',
            },
            'applied_to_samples.classifications': {
                'title': 'Classifications',
            },
            'applied_to_samples.sample_terms.term_name': {
                'title': 'Sample Term',
            },
            'applied_to_samples.targeted_sample_term.term_name': {
                'title': 'Targeted Sample Term',
            },
            'applied_to_samples.disease_terms.term_name': {
                'title': 'Disease Term',
            },
            'collections': {
                'title': 'Collections',
            },
            'status': {
                'title': 'Status'
            },
            'files.content_type': {
                'title': 'Available File Types',
            },
            'integrated_content_files.content_type': {
                'title': 'Integrated Content',
            },
            'file_set_type': {
                'title': 'File Set Type',
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
                    'associated_phenotypes.term_name',
                    'tiling_modality',
                    'guide_type',
                    'small_scale_gene_list.symbol',
                    'orf_list.gene.symbol',
                ],
            },
            {
                'title': 'Sample',
                'facet_fields': [
                    'applied_to_samples.donors.taxa',
                    'applied_to_samples.classifications',
                    'applied_to_samples.sample_terms.term_name',
                    'applied_to_samples.targeted_sample_term.term_name',
                    'applied_to_samples.disease_terms.term_name',
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
                'title': 'File Data',
                'facet_fields': [
                    'files.content_type',
                    'integrated_content_files.content_type',
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
            'small_scale_gene_list.symbol': {
                'title': 'Genes'
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
