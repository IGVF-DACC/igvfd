from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='AlignmentFile'
)
def alignment_file():
    return {
        'facets': {
            'content_type': {
                'title': 'Content Type'
            },
            'file_format': {
                'title': 'File Format'
            },
            'filtered': {
                'title': 'Filtered'
            },
            'redacted': {
                'title': 'Redacted'
            },
            'assembly': {
                'title': 'Assembly'
            },
            'transcriptome_annotation': {
                'title': 'Transcriptome Annotation'
            },
            'file_set.file_set_type': {
                'title': 'File Set Type'
            },
            'assay_titles': {
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
            'type': {
                'title': 'Object Type'
            },
        },
        'facet_groups': [
            {
                'title': 'File Details',
                'facet_fields': [
                    'content_type',
                    'file_format',
                    'filtered',
                    'redacted',
                    'assembly',
                    'transcriptome_annotation'
                ],
            },
            {
                'title': 'File Set',
                'facet_fields': [
                    'file_set.file_set_type',
                    'assay_titles',
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
                    'file_set.samples.treatments.treatment_term_name'
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
                ],
            },
        ],
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
            'reference_files': {
                'title': 'Reference Files'
            },
            'content_summary': {
                'title': 'Content Summary'
            },
            'upload_status': {
                'title': 'Upload Status'
            }
        }
    }
