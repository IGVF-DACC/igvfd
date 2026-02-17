from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='PseudobulkSet'
)
def pseudobulk_set():
    return {
        'facets': {
            'file_set_type': {
                'title': 'Pseudobulk Set Type',
                'category': 'Pseudobulk Set Details',
                'description': '',
                'optional': True
            },
            'files.assembly': {
                'title': 'Assembly',
                'category': 'Analysis Set Details',
                'description': 'The genome assembly associated with the analysis.',
                'optional': True
            },
            'files.transcriptome_annotation': {
                'title': 'Transcriptome Annotation',
                'category': 'Analysis Set Details',
                'description': 'The transcriptome annotation version of the analysis.',
                'optional': True
            },
            'donors.taxa': {
                'title': 'Taxa',
                'category': 'Sample',
                'description': 'The organism or species associated with the donor.'
            },
            'samples.classifications': {
                'title': 'Classification',
                'category': 'Sample',
                'description': 'High-level classification of the sample.',
                'optional': True
            },
            'samples.sample_terms.term_name': {
                'title': 'Sample',
                'category': 'Sample',
                'description': 'The sample name associated with the analysis set.'
            },
            'samples.targeted_sample_term.term_name': {
                'title': 'Cellular Transformation Target',
                'category': 'Sample',
                'description': 'Biosample name of the endpoint from a differentiation or reprogramming protocol.'
            },
            'samples.disease_terms.term_name': {
                'title': 'Disease',
                'category': 'Sample',
                'description': 'Disease(s) associated with the sample.'
            },
            'samples.growth_medium': {
                'title': 'Growth Medium',
                'category': 'Sample',
                'description': 'The growth medium or conditions used to culture the sample.',
                'optional': True
            },
            'files.content_type': {
                'title': 'File Type',
                'category': 'File',
                'description': 'The type of files included in the analysis set.',
                'optional': True
            },
            'files.file_format': {
                'title': 'File Format',
                'category': 'File',
                'description': 'The file formats included in the analysis set.',
                'optional': True
            },
            'controlled_access': {
                'title': 'Controlled Access',
                'category': 'File',
                'description': 'Boolean value, indicating whether access to the data is restricted or not.',
                'optional': True
            },
            'data_use_limitation_summaries': {
                'title': 'Data Use Limitation',
                'category': 'File',
                'description': 'Summaries of restrictions or limitations on data usage.',
                'optional': True
            },
            'collections': {
                'title': 'Collections',
                'category': 'Provenance',
                'description': 'Data collections the analysis set is a part of.',
                'optional': True
            },
            'lab.title': {
                'title': 'Lab',
                'category': 'Provenance',
                'description': 'Lab that generated or submitted the data.'
            },
            'award.component': {
                'title': 'Award',
                'category': 'Provenance',
                'description': 'The project component the award is associated with.',
                'optional': True
            },
            'release_timestamp': {
                'title': 'Release Date',
                'category': 'Provenance',
                'description': 'The date the analysis set was publicly released.'
            },
            'creation_timestamp': {
                'title': 'Creation Date',
                'category': 'Provenance',
                'description': 'The date the analysis set was submitted.',
                'optional': True
            },
            'status': {
                'title': 'Status',
                'category': 'Analysis Set Details',
                'description': 'The status of the analysis.'
            },
            'audit.ERROR.category': {
                'title': 'Audit Category: Error',
                'category': 'Audit',
                'description': 'Audit for errors: identifies incorrect or inconsistent metadata. Datasets flagged cannot be released until resolved.',
                'optional': True
            },
            'audit.NOT_COMPLIANT.category': {
                'title': 'Audit Category: Not Compliant',
                'category': 'Audit',
                'description': 'Audit for non-compliance: identifies data that does not meet compliance standards. Release requires special approval.',
                'optional': True
            },
            'audit.WARNING.category': {
                'title': 'Audit Category: Warning',
                'category': 'Audit',
                'description': 'Audit for warnings: flags potentially inconsistent metadata. Datasets may be released despite warnings.',
                'optional': True
            },
            'audit.INTERNAL_ACTION.category': {
                'title': 'Audit Category: Internal Action',
                'category': 'Audit',
                'description': 'Audit for internal action: identifies metadata issues that require DACC staff resolution.',
                'optional': True
            }
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
            'description': {
                'title': 'Description'
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
    name='PseudobulkSetReportView'
)
def pseudobulk_set_report_view():
    # Copy normal analysis_set config.
    config = pseudobulk_set()
    # Override columns.
    config['columns'] = {
        'summary': {
            'title': 'Summary'
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
