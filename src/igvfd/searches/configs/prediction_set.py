from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='PredictionSet'
)
def prediction_set():
    return {
        'facets': {
            'file_set_type': {
                'title': 'File Set Type',
                'default': 'True'
            },
            'scope': {
                'title': 'Prediction Scope',
                'default': 'True'
            },
            'software_versions.software.title': {
                'title': 'Software',
                'default': 'True'
            },
            'associated_phenotypes.term_name': {
                'title': 'Associated Phenotypes',
                'default': 'True'
            },
            'assessed_genes.symbol': {
                'title': 'Assessed Genes',
                'default': 'True'
            },
            'donors.taxa': {
                'title': 'Taxa',
                'default': 'True'
            },
            'samples.classifications': {
                'title': 'Classification',
                'default': 'True'
            },
            'samples.sample_terms.term_name': {
                'title': 'Sample',
                'default': 'True'
            },
            'samples.targeted_sample_term.term_name': {
                'title': 'Cellular Transformation Target',
                'default': 'True'
            },
            'samples.disease_terms.term_name': {
                'title': 'Disease',
                'default': 'True'
            },
            'samples.growth_medium': {
                'title': 'Growth Medium',
                'default': 'False'
            },
            'samples.modifications.modality': {
                'title': 'Modification',
                'default': 'True'
            },
            'samples.treatments.treatment_term_name': {
                'title': 'Treatment',
                'default': 'True'
            },
            'construct_library_sets.file_set_type': {
                'title': 'Construct Library Data',
                'default': 'False'
            },
            'construct_library_sets.selection_criteria': {
                'title': 'Construct Library Selection Criteria',
                'default': 'False'
            },
            'construct_library_sets.integrated_content_files.content_type': {
                'title': 'Construct Library Design',
                'default': 'False'
            },
            'files.assembly': {
                'title': 'Assembly',
                'default': 'True'
            },
            'files.transcriptome_annotation': {
                'title': 'Transcriptome Annotation',
                'default': 'True'
            },
            'files.content_type': {
                'title': 'File Type',
                'default': 'True'
            },
            'files.file_format': {
                'title': 'File Format',
                'default': 'True'
            },
            'collections': {
                'title': 'Collections',
                'default': 'False'
            },
            'controlled_access': {
                'title': 'Controlled Access',
                'default': 'True'
            },
            'data_use_limitation_summaries': {
                'title': 'Data Use Limitation',
                'default': 'False'
            },
            'lab.title': {
                'title': 'Lab',
                'default': 'True'
            },
            'award.component': {
                'title': 'Award',
                'default': 'True'
            },
            'release_timestamp': {
                'title': 'Release Date',
                'default': 'True'
            },
            'creation_timestamp': {
                'title': 'Creation Date',
                'default': 'False'
            },
            'status': {
                'title': 'Status',
                'default': 'True'
            },
            'audit.ERROR.category': {
                'title': 'Audit Category: Error',
                'default': 'True'
            },
            'audit.NOT_COMPLIANT.category': {
                'title': 'Audit Category: Not Compliant',
                'default': 'True'
            },
            'audit.WARNING.category': {
                'title': 'Audit Category: Warning',
                'default': 'True'
            },
            'audit.INTERNAL_ACTION.category': {
                'title': 'Audit Category: Internal Action',
                'default': 'True'
            },
            'type': {
                'title': 'Object Type',
                'default': 'False'
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
            'samples': {
                'title': 'Samples'
            },
            'summary': {
                'title': 'Summary'
            },
            'data_use_limitation_summaries': {
                'title': 'Data Use Limitation Summaries'
            },
            'controlled_access': {
                'title': 'Controlled Access'
            },
            'donors': {
                'title': 'Donors'
            },
            'scope': {
                'title': 'Prediction Scope'
            },
            'files.content_type': {
                'title': 'File Content Type'
            }
        }
    }


@search_config(
    name='PredictionSetReportView'
)
def prediction_set_report_view():
    # Copy normal prediction_set config.
    config = prediction_set()
    # Override columns.
    config['columns'] = {
        'summary': {
            'title': 'Summary'
        },
        'samples.summary': {
            'title': 'Sample Summary'
        },
        'samples.institutional_certificates': {
            'title': 'Sample Institutional Certificates'
        },
        'scope': {
            'title': 'Prediction Scope'
        },
        'files.content_type': {
            'title': 'File Content Type'
        },
        'files.file_format': {
            'title': 'File Format'
        },
        'files.assembly': {
            'title': 'File Assembly'
        },
        'associated_phenotypes.term_name': {
            'title': 'Associated Phenotypes Name'
        },
    }
    return config
