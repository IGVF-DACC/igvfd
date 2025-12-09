from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='MeasurementSet'
)
def measurement_set():
    return {
        'facets': {
            'assay_term.assay_slims': {
                'title': 'Assay',
                'category': 'Measurement Set Details',
                'description': 'High-level assay classification based on OBI assay slim terms.',
                'type': 'hierarchical',
                'subfacets': [
                    {'field': 'assay_term.term_name', 'title': 'Assay type'}
                ]
            },
            'preferred_assay_titles': {
                'title': 'Preferred Assay Titles',
                'category': 'Measurement Set Details',
                'description': 'Title of assays that generated the measurement set.'
            },
            'control_types': {
                'title': 'Control Types',
                'category': 'Measurement Set Details',
                'description': 'The type of control for the measurement set, if applicable.',
                'optional': True
            },
            'targeted_genes.symbol': {
                'title': 'Readout Gene',
                'category': 'Measurement Set Details',
                'description': 'A list of genes targeted for binding sites or used for sorting by expression.',
                'optional': True
            },
            'auxiliary_sets.file_set_type': {
                'title': 'Auxiliary Data',
                'category': 'Measurement Set Details',
                'description': 'Additional file sets that supplement or support the primary measurement set.',
                'optional': True
            },
            'functional_assay_mechanisms.term_name': {
                'title': 'Measured Mechanisms',
                'category': 'Measurement Set Details',
                'description': 'Ontological term that describes the biological processes measured by this functional assay.',
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
                'description': 'The sample term name associated with the measurement set.'
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
            'library_preparation_kit': {
                'title': 'Library Preparation Kit',
                'category': 'Library',
                'description': 'The reagant kit utilized in the library preparation procedure.',
                'optional': True
            },
            'construct_library_sets.file_set_type': {
                'title': 'Construct Library',
                'category': 'Library',
                'description': 'The type of the construct library associated with the measurement set.',
                'optional': True
            },
            'construct_library_sets.selection_criteria': {
                'title': 'Construct Library Selection Criteria',
                'category': 'Library',
                'description': 'The criteria used to select the sequence material cloned into the library.',
                'optional': True
            },
            'construct_library_sets.associated_phenotypes.term_name': {
                'title': 'Associated Phenotypes',
                'category': 'Library',
                'description': 'Ontological terms for diseases or phenotypes associated with this measurement set.',
                'optional': True
            },
            'construct_library_sets.small_scale_gene_list.symbol': {
                'title': 'Investigated Gene',
                'category': 'Library',
                'description': 'Gene symbols for specific genes the construct library was designed to target.',
                'optional': True
            },
            'sequencing_library_types': {
                'title': 'Library Material',
                'category': 'Library',
                'description': 'Description of the libraries sequenced in this measurement set.',
                'optional': True
            },
            'files.sequencing_platform.term_name': {
                'title': 'Sequencing Platform',
                'category': 'File',
                'description': 'The sequencing instrument or platform used to generate raw data.',
                'optional': True
            },
            'files.content_type': {
                'title': 'File Types',
                'category': 'File',
                'description': 'The type of files included in the measurement set.'
            },
            'files.file_format': {
                'title': 'File Format',
                'category': 'File',
                'description': 'The file formats included in the measurement set.',
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
                'description': 'Data collections the measurement set is a part of.',
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
                'description': 'The date the measurement set was publicly released.'
            },
            'creation_timestamp': {
                'title': 'Creation Date',
                'category': 'Provenance',
                'description': 'The date the measurement set was submitted.',
                'optional': True
            },
            'status': {
                'title': 'Status',
                'category': 'Measurement Set Details',
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
            'assay_titles': {
                'title': 'Assay Term Names'
            },
            'preferred_assay_titles': {
                'title': 'Preferred Assay Titles'
            },
            'sequencing_library_types': {
                'title': 'Sequencing Library Types'
            },
            'targeted_genes.symbol': {
                'title': 'Assay Targeted Genes'
            },
            'protocols': {
                'title': 'Protocols'
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
            'functional_assay_mechanisms.term_name': {
                'title': 'Measured Mechanism'
            }
        }
    }


@search_config(
    name='MeasurementSetReportView'
)
def measurement_set_report_view():
    # Copy normal measurement_set config.
    config = measurement_set()
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
        'preferred_assay_titles': {
            'title': 'Preferred Assay Titles'
        },
        'assay_titles': {
            'title': 'Assay Term Names'
        },
        'files.content_type': {
            'title': 'File Content Type'
        },
        'files.file_format': {
            'title': 'File Format'
        },
    }
    return config


@search_config(
    name='AssaySummary'
)
def assay_summary():
    return {
        'matrix': {
            'x': {
                'group_by': 'samples.classifications',
                'label': 'Classifications'
            },
            'y': {
                'group_by': ['assay_term.assay_slims', 'assay_term.term_name', 'preferred_assay_titles'],
                'label': 'Samples'
            }
        }
    }
