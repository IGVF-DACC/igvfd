from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='AuxiliarySet'
)
def auxiliary_set():
    return {
        'facets': {
            'file_set_type': {
                'title': 'File Set Type'
            },
            'measurement_sets.preferred_assay_title': {
                'title': 'Assay',
            },
            'files.assembly': {
                'title': 'Assembly',
            },
            'files.transcriptome_annotation': {
                'title': 'Transcriptome Annotation',
            },
            'donors.taxa': {
                'title': 'Taxa'
            },
            'samples.classifications': {
                'title': 'Classification',
            },
            'samples.sample_terms.term_name': {
                'title': 'Sample',
            },
            'samples.targeted_sample_term.term_name': {
                'title': 'Cellular Transformation Target',
            },
            'samples.disease_terms.term_name': {
                'title': 'Disease',
            },
            'samples.modifications.modality': {
                'title': 'Modification',
            },
            'samples.treatments.treatment_term_name': {
                'title': 'Treatment',
            },
            'sequencing_library_types': {
                'title': 'Library Type',
            },
            'files.content_type': {
                'title': 'File Types',
            },
            'files.file_format': {
                'title': 'File Format',
            },
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award'
            },
            'collections': {
                'title': 'Collections',
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
        'facet_groups': [
            {
                'title': 'Auxiliary Set Details',
                'facet_fields': [
                    'file_set_type',
                    'measurement_sets.preferred_assay_title',
                    'files.assembly',
                    'files.transcriptome_annotation'
                ],
            },
            {
                'title': 'Sample',
                'facet_fields': [
                    'donors.taxa',
                    'samples.classifications',
                    'samples.sample_terms.term_name',
                    'samples.targeted_sample_term.term_name',
                    'samples.disease_terms.term_name',
                    'samples.modifications.modality',
                    'samples.treatments.treatment_term_name',
                    'sequencing_library_types',
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
                    'files.file_format'
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
            'alternate_accessions': {
                'title': 'Alternate Accessions'
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
            'samples': {
                'title': 'Samples'
            },
            'donors': {
                'title': 'Donors'
            },
            'summary': {
                'title': 'Summary'
            },
            'measurement_sets': {
                'title': 'Measurement Sets'
            }
        }
    }
