from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='CuratedSet'
)
def curated_set():
    return {
        'facets': {
            'file_set_type': {
                'title': 'File Set Type'
            },
            'assemblies': {
                'title': 'Assemblies'
            },
            'transcriptome_annotations': {
                'title': 'Transcriptome Annotations'
            },
            'taxa': {
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
            'files.content_type': {
                'title': 'File Type',
            },
            'files.file_format': {
                'title': 'File Format',
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
                'title': 'Curated Set Details',
                'facet_fields': [
                    'file_set_type',
                    'taxa',
                    'assemblies',
                    'transcriptome_annotations',
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
                'title': 'Files',
                'facet_fields': [
                    'files.content_type',
                    'files.file_format',
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
            'alternate_accessions': {
                'title': 'Alternate Accessions'
            },
            'uuid': {
                'title': 'UUID'
            },
            'aliases': {
                'title': 'Aliases'
            },
            'description': {
                'title': 'Description'
            },
            'status': {
                'title': 'Status'
            },
            'samples': {
                'title': 'Samples'
            },
            'donors': {
                'title': 'Donors'
            },
            'lab': {
                'title': 'Lab'
            },
            'award': {
                'title': 'Award'
            },
            'taxa': {
                'title': 'Taxa'
            },
            'assemblies': {
                'title': 'Assemblies'
            },
            'transcriptome_annotations': {
                'title': 'Transcriptome Annotations'
            },
            'file_set_type': {
                'title': 'File Set Type'
            },
            'summary': {
                'title': 'Summary'
            }
        }
    }
