from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='File'
)
def file():
    return {
        'facets': {
            'content_type': {
                'title': 'Content Type',
                'description': 'The type of content in the file.',
                'category': 'File Details'
            },
            'file_format': {
                'title': 'File Format',
                'description': 'The file format or extension of the file.',
                'category': 'File Details'
            },
            'file_format_type': {
                'title': 'File Format Type',
                'description': 'The subtype of bed files.',
                'optional': True,
                'category': 'File Details'
            },
            'assembly': {
                'title': 'Assembly',
                'description': 'The genome assembly associated with the file.',
                'category': 'File Details'
            },
            'transcriptome_annotation': {
                'title': 'Transcriptome Annotation',
                'description': 'The transcriptome annotation version of the file.',
                'category': 'File Details'
            },
            'controlled_access': {
                'title': 'Controlled Access',
                'description': 'Boolean value, indicating whether access to the data is restricted or not.',
                'optional': True,
                'category': 'File Details'
            },
            'file_set.data_use_limitation_summaries': {
                'title': 'Data Use Limitation',
                'description': 'Summaries of restrictions or limitations on data usage.',
                'optional': True,
                'category': 'File Details'
            },
            'file_size': {
                'title': 'File Size',
                'description': 'File size specified in bytes.',
                'optional': True,
                'category': 'File Details',
                'type': 'stats'
            },
            'sequencing_platform.term_name': {
                'title': 'Sequencing Platform',
                'description': 'The measurement device used to produce sequencing data.',
                'category': 'File Details'
            },
            'externally_hosted': {
                'title': 'Externally Hosted',
                'description': 'Indicates whether the file is externally hosted and not stored on portal.',
                'optional': True,
                'category': 'File Details'
            },
            'file_format_specifications.standardized_file_format': {
                'title': 'Standardized Format',
                'description': 'Boolean value, specifying whether this format is an IGVF-standardized file format defined by Focus Groups or produced by a uniform pipeline.',
                'optional': True,
                'category': 'File Details'
            },
            'workflows.name': {
                'title': 'Workflows',
                'description': 'The workflows used to produce this file.',
                'optional': True,
                'category': 'Processing Details'
            },
            'workflows.uniform_pipeline': {
                'title': 'Uniformly Processed',
                'description': 'The status of the single cell or Perturb-seq uniform pipeline processing for this file.',
                'optional': True,
                'category': 'Processing Details'
            },
            'file_set.file_set_type': {
                'title': 'File Set Type',
                'description': 'The type of file set the file belongs to.',
                'optional': True,
                'category': 'File Set Details'
            },
            'assay_titles': {
                'title': 'Assay',
                'description': 'High-level assay classification based on OBI assay slim terms.',
                'optional': True,
                'category': 'File Set Details'
            },
            'preferred_assay_titles': {
                'title': 'Preferred Assay Titles',
                'description': 'Title of assays that generated the measurement set.',
                'category': 'File Set Details'
            },
            'cell_type_annotation.term_name': {
                'title': 'Annotated Cell Type',
                'description': 'The inferred cell type this file is associated with based on single-cell expression profiling.',
                'optional': True,
                'category': 'File Set Details'
            },
            'file_set.samples.taxa': {
                'title': 'Taxa',
                'description': 'The organism or species associated with the donor.',
                'category': 'Sample'
            },
            'file_set.samples.classifications': {
                'title': 'Classification',
                'description': 'High-level classification of the sample.',
                'optional': True,
                'category': 'Sample'
            },
            'file_set.samples.sample_terms.term_name': {
                'title': 'Sample',
                'description': 'The sample term name associated with the prediction set.',
                'optional': True,
                'category': 'Sample'
            },
            'file_set.samples.targeted_sample_term.term_name': {
                'title': 'Cellular Transformation Target',
                'description': 'Ontology term identifying the targeted endpoint sample resulting from differentiation or reprogramming.',
                'category': 'Sample'
            },
            'file_set.samples.disease_terms.term_name': {
                'title': 'Disease',
                'description': 'Ontology term of the disease associated with the sample.',
                'optional': True,
                'category': 'Sample'
            },
            'file_set.samples.modifications.modality': {
                'title': 'Modification',
                'description': 'The type of modification applied to the sample.',
                'optional': True,
                'category': 'Sample'
            },
            'file_set.samples.treatments.treatment_term_name': {
                'title': 'Treatment',
                'description': 'Treatments applied to the sample with the purpose of perturbation.',
                'optional': True,
                'category': 'Sample'
            },
            'integrated_in.samples.sample_terms.term_name': {
                'title': 'Sample Integrated In',
                'description': 'The type of sample the construct library was integrated in.',
                'optional': True,
                'category': 'Sample'
            },
            'integrated_in.file_set_type': {
                'title': 'Library Type',
                'description': 'Construct library set(s) that this file was used for in insert design.',
                'optional': True,
                'category': 'Library'
            },
            'integrated_in.associated_phenotypes.term_name': {
                'title': 'Associated Phenotype',
                'description': 'Ontological terms for diseases or phenotypes associated with this file.',
                'optional': True,
                'category': 'Library'
            },
            'integrated_in.small_scale_gene_list.symbol': {
                'title': 'Construct Target Genes',
                'description': 'Gene symbols for specific genes the construct library was designed to target.',
                'optional': True,
                'category': 'Library'
            },
            'sequencing_kit': {
                'title': 'Sequencing Kit',
                'description': 'A reagent kit used with a library to prepare it for sequencing.',
                'optional': True,
                'category': 'Library'
            },
            'collections': {
                'title': 'Collections',
                'description': 'Data collections the measurement set is a part of.',
                'optional': True,
                'category': 'Provenance'
            },
            'lab.title': {
                'title': 'Lab',
                'description': 'Lab that generated or submitted the data.',
                'category': 'Provenance'
            },
            'award.component': {
                'title': 'Award',
                'description': 'Grant associated with the data.',
                'optional': True,
                'category': 'Provenance'
            },
            'release_timestamp': {
                'title': 'Release Date',
                'description': 'The date the measurement set was publicly released.',
                'optional': True,
                'category': 'Provenance'
            },
            'creation_timestamp': {
                'title': 'Creation Date',
                'description': 'The date the measurement set was submitted.',
                'optional': True,
                'category': 'Provenance'
            },
            'status': {
                'title': 'Status',
                'description': 'The date the measurement set was publicly released.',
                'optional': False,
                'category': 'File Details'
            },
            'upload_status': {
                'title': 'Upload Status',
                'description': 'The date the measurement set was submitted.',
                'optional': True,
                'category': 'Audit'
            },
            'type': {
                'title': 'Object Type',
                'description': 'The status of the analysis.',
                'optional': True,
                'category': 'Audit'
            },
            'audit.ERROR.category': {
                'title': 'Audit Category: Error',
                'description': 'Audit for errors: identifies incorrect or inconsistent metadata. Datasets flagged cannot be released until resolved.',
                'optional': True,
                'category': 'Audit'
            },
            'audit.NOT_COMPLIANT.category': {
                'title': 'Audit Category: Not Compliant',
                'description': 'Audit for non-compliance: identifies data that does not meet compliance standards. Release requires special approval.',
                'optional': True,
                'category': 'Audit'
            },
            'audit.WARNING.category': {
                'title': 'Audit Category: Warning',
                'description': 'Audit for warnings: flags potentially inconsistent metadata. Datasets may be released despite warnings.',
                'optional': True,
                'category': 'Audit'
            },
            'audit.INTERNAL_ACTION.category': {
                'title': 'Audit Category: Internal Action',
                'description': 'Audit for internal action: identifies metadata issues that require DACC staff resolution.',
                'optional': True,
                'category': 'Audit'
            }
        }
    }


@search_config(
    name='FileReportView'
)
def file_report_view():
    # Copy normal file config.
    config = file()
    # Override columns.
    config['columns'] = {
        'content_type': {
            'title': 'Content Type'
        },
        'file_format': {
            'title': 'File Format'
        },
        'assembly': {
            'title': 'Assembly'
        },
        'transcriptome_annotation': {
            'title': 'Transcriptome Annotation'
        },
        'sequencing_platform.term_name': {
            'title': 'Sequencing Platform'
        },
        'preferred_assay_titles': {
            'title': 'Preferred Assay Titles'
        },
        'file_set.samples.taxa': {
            'title': 'Taxa'
        },
        'file_set.samples.sample_terms.term_name': {
            'title': 'Sample'
        },
        'file_set.samples.targeted_sample_term.term_name': {
            'title': 'Cellular Transformation Target'
        },
        'lab.title': {
            'title': 'Lab'
        },
        'status': {
            'title': 'Status'
        }
    }
    return config
