from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='ModelSet'
)
def model_set():
    return {
        'facets': {
            'file_set_type': {
                'title': 'File Set Type'
            },
            'prediction_objects': {
                'title': 'Prediction Subject'
            },
            'assessed_genes': {
                'title': 'Assessed Gene'
            },
            'construct_library_sets.file_set_type': {
                'title': 'Construct Library Data'
            },
            'donors.taxa': {
                'title': 'Taxa',
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
                'title': 'Modification'
            },
            'samples.treatments.treatment_term_name': {
                'title': 'Treatment'
            },
            'files.content_type': {
                'title': 'File Types',
            },
            'files.file_format': {
                'title': 'File Format',
            },
            'software_versions.software.title': {
                'title': 'Software',
            },
            'construct_library_sets.integrated_content_files.content_type': {
                'title': 'Construct Library Design'
            },
            'collections': {
                'title': 'Collections',
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
            'externally_hosted': {
                'title': 'Externally Hosted'
            },
            'type': {
                'title': 'Object Type',
            },
        },
        'facet_groups': [
            {
                'title': 'Model Set Details',
                'facet_fields': [
                    'file_set_type',
                    'prediction_objects',
                    'assessed_genes',
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
                'title': 'Software',
                'facet_fields': [
                    'software_versions.software.title'
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
                    'externally_hosted',
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
            'status': {
                'title': 'Status'
            },
            'lab': {
                'title': 'Lab'
            },
            'award': {
                'title': 'Award'
            },
            'model_name': {
                'title': 'Model Name'
            },
            'file_set_type': {
                'title': 'File Set Type'
            },
            'prediction_objects': {
                'title': 'Prediction Objects'
            },
            'summary': {
                'title': 'Summary'
            },
            'assessed_genes': {
                'title': 'Assessed Genes'
            }
        }
    }
