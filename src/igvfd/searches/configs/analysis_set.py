from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='AnalysisSet'
)
def analysis_set():
    return {
        'facets': {
            'file_set_type': {
                'title': 'Analysis Set Type',
                'default': 'True',
            },
            'assay_titles': {
                'title': 'Assay Term Names',
                'default': 'True'
            },
            'preferred_assay_titles': {
                'title': 'Preferred Assay Titles',
                'default': 'True'
            },
            'workflows.uniform_pipeline': {
                'title': 'Uniformly Processed',
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
                'default': 'True',
            },
            'samples.disease_terms.term_name': {
                'title': 'Disease',
                'default': 'True',
            },
            'samples.growth_medium': {
                'title': 'Growth Medium',
                'default': 'False'
            },
            'samples.modifications.modality': {
                'title': 'Modification',
                'default': 'False'
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
            'construct_library_sets.small_scale_gene_list.symbol': {
                'title': 'Investigated Gene',
                'default': 'False'
            },
            'targeted_genes.symbol': {
                'title': 'Readout Gene',
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
            'uuid': {
                'title': 'UUID'
            },
            'aliases': {
                'title': 'Aliases'
            },
            'status': {
                'title': 'Status'
            },
            'samples': {
                'title': 'Samples'
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
            'lab': {
                'title': 'Lab'
            },
            'award': {
                'title': 'Award'
            },
            'input_file_sets': {
                'title': 'Input File Sets'
            },
            'sample_summary': {
                'title': 'Simplified Sample Summary'
            },
            'summary': {
                'title': 'Summary'
            },
            'donors.taxa': {
                'title': 'Taxa'
            },
            'file_set_type': {
                'title': 'File Set Type'
            },
            'protocols': {
                'title': 'Protocols'
            },
            'functional_assay_mechanisms.term_name': {
                'title': 'Functional Assay Mechanisms'
            },
            'files.content_type': {
                'title': 'File Content Type'
            }
        },
    }


@search_config(
    name='AnalysisSetReportView'
)
def analysis_set_report_view():
    # Copy normal analysis_set config.
    config = analysis_set()
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
        'sample_summary': {
            'title': 'Simplified Sample Summary'
        },
        'assay_titles': {
            'title': 'Assay Term Names'
        },
        'preferred_assay_titles': {
            'title': 'Preferred Assay Titles'
        },
        'file_set_type': {
            'title': 'File Set Type'
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
    }
    return config
