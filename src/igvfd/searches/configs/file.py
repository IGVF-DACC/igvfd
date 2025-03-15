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
            'sequencing_platform.term_name': {
                'title': 'Sequencing Platform'
            },
            'file_set.file_set_type': {
                'title': 'File Set Type'
            },
            'assay_titles': {
                'title': 'Assay'
            },
            'file_set.assay_term.term_name': {
                'title': 'Assay Term'
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
            'workflow.name': {
                'title': 'Workflow'
            },
            'workflow.uniform_pipeline': {
                'title': 'Uniformly Processed'
            },
            'integrated_in.file_set_type': {
                'title': 'Library Type'
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
        },
        'facet_groups': [
            {
                'title': 'File Details',
                'facet_fields': [
                    'content_type',
                    'file_format',
                    'file_format_type',
                    'assembly',
                    'transcriptome_annotation',
                    'controlled_access',
                    'sequencing_platform.term_name',
                    'workflow.name',
                    'workflow.uniform_pipeline',
                ],
            },
            {
                'title': 'File Set',
                'facet_fields': [
                    'file_set.file_set_type',
                    'assay_titles',
                    'file_set.assay_term.term_name'
                    'cell_type_annotation.term_name',
                    'integrated_in.file_set_type',
                ],
            },
            {
                'title': 'Sample',
                'facet_fields': [
                    'file_set.samples.taxa',
                    'file_set.samples.classifications',
                    'file_set.samples.sample_terms.term_name',
                    'file_set.samples.targeted_sample_term.term_name',
                    'file_set.samples.disease_terms.term_name',
                    'file_set.samples.modifications.modality',
                    'file_set.samples.treatments.treatment_term_name',
                    'sequencing_kit',
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
                    'upload_status',
                    'status',
                    'audit.ERROR.category',
                    'audit.NOT_COMPLIANT.category',
                    'audit.WARNING.category',
                    'audit.INTERNAL_ACTION.category',
                    'externally_hosted',
                ],
            },
        ]
    }
