from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='ConstructLibrarySet'
)
def construct_library_set():
    return {
        'facets': {
            'file_set_type': {
                'title': 'File Set Type'
            },
            'selection_criteria': {
                'title': 'Selection Criteria'
            },
            'scope': {
                'title': 'Scope'
            },
            'associated_phenotypes.term_name': {
                'title': 'Associated Phenotypes'
            },
            'small_scale_gene_list.symbol': {
                'title': 'Targeted Genes'
            },
            'orf_list.gene.symbol': {
                'title': 'Open Reading Frame Gene'
            },
            'control_type': {
                'title': 'Control Type'
            },
            'tiling_modality': {
                'title': 'CRISPR Tiling Modality'
            },
            'guide_type': {
                'title': 'CRISPR Guide Type'
            },
            'assay_titles': {
                'title': 'Assay',
            },
            'integrated_content_files.content_type': {
                'title': 'Integrated Content',
            },
            'applied_to_samples.donors.taxa': {
                'title': 'Taxa',
            },
            'applied_to_samples.classifications': {
                'title': 'Classification',
            },
            'applied_to_samples.sample_terms.term_name': {
                'title': 'Sample',
            },
            'applied_to_samples.targeted_sample_term.term_name': {
                'title': 'Cellular Transformation Target',
            },
            'applied_to_samples.disease_terms.term_name': {
                'title': 'Disease',
            },
            'applied_to_samples.modifications.modality': {
                'title': 'Modification',
            },
            'applied_to_samples.treatments.treatment_term_name': {
                'title': 'Treatment'
            },
            'applied_to_samples.nucleic_acid_delivery': {
                'title': 'Nucleic Acid Delivery Method'
            },
            'files.content_type': {
                'title': 'File Types',
            },
            'files.file_format': {
                'title': 'File Format',
            },
            'collections': {
                'title': 'Collections',
            },
            'controlled_access': {
                'title': 'Controlled Access',
            },
            'data_use_limitation_summaries': {
                'title': 'Data Use Limitation',
            },
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award'
            },
            'release_timestamp': {
                'title': 'Release Date',
            },
            'creation_timestamp': {
                'title': 'Creation Date',
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
            'type': {
                'title': 'Object Type',
            },
        },
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
            'data_use_limitation_summaries': {
                'title': 'Data Use Limitation Summaries'
            },
            'controlled_access': {
                'title': 'Controlled Access'
            },
            'selection_criteria': {
                'title': 'Selection Criteria'
            },
            'small_scale_gene_list.symbol': {
                'title': 'Genes'
            },
            'associated_phenotypes.term_name': {
                'title': 'Associated Phenotypes Name'
            },
            'alternate_accessions': {
                'title': 'Alternate Accessions'
            },
            'summary': {
                'title': 'Summary'
            },
        }
    }
