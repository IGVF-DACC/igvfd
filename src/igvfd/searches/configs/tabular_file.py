from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='TabularFile'
)
def tabular_file():
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
            'cell_type_annotation.term_name': {
                'title': 'Annotated Cell Type'
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
            'file_set.file_set_type': {
                'title': 'File Set Type'
            },
            'assay_titles': {
                'title': 'Preferred Assay Title'
            },
            'file_set.assay_term.term_name': {
                'title': 'Assay'
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
            'workflow.name': {
                'title': 'Workflow'
            },
            'workflow.uniform_pipeline': {
                'title': 'Uniformly Processed'
            },
            'file_format_specifications.standardized': {
                'title': 'Standardized Format'
            },
            'integrated_in.file_set_type': {
                'title': 'Library Type'
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
            'upload_status': {
                'title': 'Upload Status'
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
            'externally_hosted': {
                'title': 'Externally Hosted'
            },
            'type': {
                'title': 'Object Type'
            },
        },
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'accession': {
                'title': 'Accession'
            },
            'alternate_accessions': {
                'title': 'Alternate Accessions'
            },
            'content_type': {
                'title': 'Content Type'
            },
            'file_format': {
                'title': 'File Format'
            },
            'lab': {
                'title': 'Lab'
            },
            'status': {
                'title': 'Status'
            },
            'file_set': {
                'title': 'File Set'
            },
            'assembly': {
                'title': 'Assembly'
            },
            'transcriptome_annotation': {
                'title': 'Transcriptome Annotation'
            },
            'upload_status': {
                'title': 'Upload Status'
            },
            'file_set.@type': {
                'title': 'File Set @Type'
            }
        }
    }
