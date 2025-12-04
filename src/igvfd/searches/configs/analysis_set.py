from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='AnalysisSet'
)
def analysis_set():
    return {
        'facets': {
            'file_set_type': {
                'title': 'Analysis Set Type',
                'category': 'Analysis Set Details',
                'description': 'The category of analysis set. Intermediate analysis are not final result of an experiment and typically used as input to a principal analysis. Principal analysis are final, core analysis.',
                'optional': True
            },
            'assay_titles': {
                'title': 'Assay Term Names',
                'category': 'Analysis Set Details',
                'description': 'Assay term names from Ontology of Biomedical Investigations (OBI) for assays.',
                'optional': True
            },
            'preferred_assay_titles': {
                'title': 'Preferred Assay Titles',
                'category': 'Analysis Set Details',
                'description': 'Title of assays that produced data analyzed in the analysis sets.'
            },
            'workflows.uniform_pipeline': {
                'title': 'Uniformly Processed',
                'category': 'Analysis Set Details',
                'description': 'The status of the single cell or Perturb-seq uniform pipeline processing for this analysis set.',
                'optional': True
            },
            'targeted_genes.symbol': {
                'title': 'Readout Gene',
                'category': 'Analysis Set Details',
                'description': 'A list of genes targeted by the input measurement sets assays for binding sites or used for sorting by expression.',
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
                'description': 'The sample term name associated with the analysis set.'
            },
            'samples.targeted_sample_term.term_name': {
                'title': 'Cellular Transformation Target',
                'category': 'Sample',
                'description': 'Ontology term identifying the targeted endpoint sample resulting from differentation or reprogramming.'
            },
            'samples.disease_terms.term_name': {
                'title': 'Disease',
                'category': 'Sample',
                'description': 'Ontology term of the disease associated with the sample.'
            },
            'samples.growth_medium': {
                'title': 'Growth Medium',
                'category': 'Sample',
                'description': 'The growth medium or conditions used to culture the sample.',
                'optional': True
            },
            'samples.modifications.modality': {
                'title': 'Modification',
                'category': 'Sample',
                'description': 'The type of modification applied to the sample.',
                'optional': True
            },
            'samples.treatments.treatment_term_name': {
                'title': 'Treatment',
                'category': 'Sample',
                'description': 'Treatments applied to the sample with the purpose of perturbation.',
                'optional': True
            },
            'construct_library_sets.file_set_type': {
                'title': 'Construct Library Data',
                'category': 'Library',
                'description': 'The type of the construct library associated with the analysis set.',
                'optional': True
            },
            'construct_library_sets.selection_criteria': {
                'title': 'Construct Library Selection Criteria',
                'category': 'Library',
                'description': 'The criteria used to select the sequence material cloned into the library.',
                'optional': True
            },
            'construct_library_sets.integrated_content_files.content_type': {
                'title': 'Construct Library Design',
                'category': 'Library',
                'description': 'Sequence material of interest either used for insert design or directly cloned into vectors in the library.',
                'optional': True
            },
            'construct_library_sets.small_scale_gene_list.symbol': {
                'title': 'Investigated Gene',
                'category': 'Library',
                'description': 'Gene symbols for specific genes the construct library was designed to target.',
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
                'description': 'Grant associated with the data.',
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
            'type': {
                'title': 'Object Type',
                'category': 'Provenance',
                'description': 'The type of object represented in the database.',
                'optional': True
            },
            'status': {
                'title': 'Status',
                'category': 'Quality',
                'description': 'The status of the analysis.'
            },
            'audit.ERROR.category': {
                'title': 'Audit Category: Error',
                'category': 'Quality',
                'description': 'Audit for errors: identifies incorrect or inconsistent metadata. Datasets flagged cannot be released until resolved.',
                'optional': True
            },
            'audit.NOT_COMPLIANT.category': {
                'title': 'Audit Category: Not Compliant',
                'category': 'Quality',
                'description': 'Audit for non-compliance: identifies data that does not meet compliance standards. Release requires special approval.',
                'optional': True
            },
            'audit.WARNING.category': {
                'title': 'Audit Category: Warning',
                'category': 'Quality',
                'description': 'Audit for warnings: flags potentially inconsistent metadata. Datasets may be released despite warnings.',
                'optional': True
            },
            'audit.INTERNAL_ACTION.category': {
                'title': 'Audit Category: Internal Action',
                'category': 'Quality',
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
