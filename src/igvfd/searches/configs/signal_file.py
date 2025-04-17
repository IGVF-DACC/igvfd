from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='SignalFile'
)
def signal_file():
    return {
        'facets': {
            'content_type': {
                'title': 'Content Type'
            },
            'file_format': {
                'title': 'File Format'
            },
            'assembly': {
                'title': 'Assembly'
            },
            'transcriptome_annotation': {
                'title': 'Transcriptome Annotation'
            },
            'strand_specificity': {
                'title': 'Strand Specificity'
            },
            'filtered': {
                'title': 'Filtered'
            },
            'normalized': {
                'title': 'Normalized'
            },
            'cell_type_annotation.term_name': {
                'title': 'Annotated Cell Type'
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
            'collections': {
                'title': 'Collections'
            },
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award'
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
            'content_summary': {
                'title': 'Content Summary'
            },
            'upload_status': {
                'title': 'Upload Status'
            },
            'file_set.@type': {
                'title': 'File Set @Type'
            }
        }
    }
