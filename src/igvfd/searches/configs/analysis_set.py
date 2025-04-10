from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='AnalysisSet'
)
def analysis_set():
    return {
        'facets': {
            'file_set_type': {
                'title': 'Analysis Set Type',
            },
            'assay_titles': {
                'title': 'Assay'
            },
            'workflows.uniform_pipeline': {
                'title': 'Uniformly Processed'
            },
            'files.assembly': {
                'title': 'Assembly',
            },
            'files.transcriptome_annotation': {
                'title': 'Transcriptome Annotation',
            },
            'construct_library_sets.file_set_type': {
                'title': 'Construct Library Data'
            },
            'donors.taxa': {
                'title': 'Taxa',
            },
            'samples.classifications': {
                'title': 'Classification'
            },
            'samples.sample_terms.term_name': {
                'title': 'Sample'
            },
            'samples.targeted_sample_term.term_name': {
                'title': 'Cellular Transformation Target'
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
                'title': 'File Type',
            },
            'files.file_format': {
                'title': 'File Format',
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
            'title': 'Assay'
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
