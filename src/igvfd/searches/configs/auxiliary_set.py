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
            'assay_titles': {
                'title': 'Assay Term Names'
            },
            'preferred_assay_titles': {
                'title': 'Preferred Assay Titles'
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
            'samples.growth_medium': {
                'title': 'Growth Medium',
            },
            'samples.modifications.modality': {
                'title': 'Modification',
            },
            'samples.treatments.treatment_term_name': {
                'title': 'Treatment',
            },
            'construct_library_sets.file_set_type': {
                'title': 'Construct Library'
            },
            'construct_library_sets.selection_criteria': {
                'title': 'Construct Library Selection Criteria'
            },
            'construct_library_sets.integrated_content_files.content_type': {
                'title': 'Construct Library Design'
            },
            'construct_library_sets.associated_phenotypes.term_name': {
                'title': 'Construct Library Associated Phenotypes'
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
            'data_use_limitation_summaries': {
                'title': 'Data Use Limitation Summaries'
            },
            'controlled_access': {
                'title': 'Controlled Access'
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
