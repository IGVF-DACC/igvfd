from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='ImageFile'
)
def image_file():
    return {
        'facets': {
            'content_type': {
                'title': 'Content Type'
            },
            'file_format': {
                'title': 'File Format'
            },
            'file_size': {
                'title': 'File Size',
                'type': 'stats'
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
            'file_set.samples.taxa': {
                'title': 'Taxa'
            },
            'file_set.samples.classifications': {
                'title': 'Classification'
            },
            'file_set.samples.sample_terms.term_name': {
                'title': 'Sample'
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
            'upload_status': {
                'title': 'Upload Status'
            },
            'file_set.@type': {
                'title': 'File Set @Type'
            }
        }
    }
