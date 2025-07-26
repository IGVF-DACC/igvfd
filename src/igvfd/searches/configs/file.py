from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='File'
)
def file():
    return {
        'facets': {
            'content_type': {
                'title': 'Content Type'
            },
            'file_format': {
                'title': 'File Format'
            },
            'file_format_type': {
                'title': 'File Format Type'
            },
            'assembly': {
                'title': 'Assembly'
            },
            'transcriptome_annotation': {
                'title': 'Transcriptome Annotation'
            },
            'controlled_access': {
                'title': 'Controlled Access'
            },
            'file_set.data_use_limitation_summaries': {
                'title': 'Data Use Limitation'
            },
            'file_size': {
                'title': 'File Size',
                'type': 'stats'
            },
            'sequencing_platform.term_name': {
                'title': 'Sequencing Platform'
            },
            'file_set.file_set_type': {
                'title': 'File Set Type'
            },
            'assay_titles': {
                'title': 'Assay Term Names'
            },
            'preferred_assay_titles': {
                'title': 'Preferred Assay Titles'
            },
            'cell_type_annotation.term_name': {
                'title': 'Annotated Cell Type'
            },
            'file_set.samples.taxa': {
                'title': 'Taxa'
            },
            'file_set.samples.sample_terms.term_name': {
                'title': 'Sample'
            },
            'file_set.samples.classifications': {
                'title': 'Classification'
            },
            'file_set.samples.targeted_sample_term.term_name': {
                'title': 'Cellular Transformation Target'
            },
            'file_set.samples.disease_terms.term_name': {
                'title': 'Disease'
            },
            'file_set.samples.modifications.modality': {
                'title': 'Modification'
            },
            'file_set.samples.treatments.treatment_term_name': {
                'title': 'Treatment'
            },
            'workflows.name': {
                'title': 'Workflows'
            },
            'workflows.uniform_pipeline': {
                'title': 'Uniformly Processed'
            },
            'file_format_specifications.standardized_file_format': {
                'title': 'Standardized Format'
            },
            'integrated_in.file_set_type': {
                'title': 'Library Type'
            },
            'integrated_in.associated_phenotypes.term_name': {
                'title': 'Associated Phenotype'
            },
            'integrated_in.small_scale_gene_list.symbol': {
                'title': 'Construct Target Genes'
            },
            'integrated_in.applied_to_samples.sample_terms.term_name': {
                'title': 'Sample Integrated In'
            },
            'sequencing_kit': {
                'title': 'Sequencing Kit'
            },
            'collections': {
                'title': 'Collections'
            },
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award',
            },
            'status': {
                'title': 'Status'
            },
            'upload_status': {
                'title': 'Upload Status'
            },
            'type': {
                'title': 'Object Type'
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
            'externally_hosted': {
                'title': 'Externally Hosted'
            }
        }
    }
