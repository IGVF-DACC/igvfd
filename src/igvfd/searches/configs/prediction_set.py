from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='PredictionSet'
)
def prediction_set():
    return {
        'facets': {
            'file_set_type': {
                'title': 'File Set Type',
                'category': 'Prediction Set Details',
                'description': 'The category of prediction set.'
            },
            'scope': {
                'title': 'Prediction Scope',
                'optional': True,
                'category': 'Prediction Set Details',
                'description': 'The scope or scale that this prediction set is designed to target.'
            },
            'software_versions.software.title': {
                'title': 'Software',
                'category': 'Prediction Set Details',
                'description': 'The software used to produce this prediction.'
            },
            'associated_phenotypes.term_name': {
                'title': 'Associated Phenotypes',
                'category': 'Prediction Set Details',
                'description': 'Ontological terms for diseases or phenotypes associated with this prediction set.'
            },
            'assessed_genes.symbol': {
                'title': 'Assessed Genes',
                'optional': True,
                'category': 'Prediction Set Details',
                'description': 'A list of gene(s) assessed in this prediction set, especially those investigated for functional impacts.'
            },
            'donors.taxa': {
                'title': 'Taxa',
                'optional': True,
                'category': 'Sample',
                'description': 'The organism or species associated with the donor.'
            },
            'samples.classifications': {
                'title': 'Classification',
                'optional': True,
                'category': 'Sample',
                'description': 'High-level classification of the sample.'
            },
            'samples.sample_terms.term_name': {
                'title': 'Sample',
                'category': 'Sample',
                'description': 'The sample term name associated with the prediction set.'
            },
            'samples.targeted_sample_term.term_name': {
                'title': 'Cellular Transformation Target',
                'optional': True,
                'category': 'Sample',
                'description': 'Ontology term identifying the targeted endpoint sample resulting from differentiation or reprogramming.'
            },
            'samples.disease_terms.term_name': {
                'title': 'Disease',
                'optional': True,
                'category': 'Sample',
                'description': 'Ontology term of the disease associated with the sample.'
            },
            'samples.growth_medium': {
                'title': 'Growth Medium',
                'optional': True,
                'category': 'Sample',
                'description': 'The growth medium or conditions used to culture the sample.'
            },
            'samples.modifications.modality': {
                'title': 'Modification',
                'optional': True,
                'category': 'Sample',
                'description': 'The type of modification applied to the sample.'
            },
            'samples.treatments.treatment_term_name': {
                'title': 'Treatment',
                'optional': True,
                'category': 'Sample',
                'description': 'Treatments applied to the sample with the purpose of perturbation.'
            },
            'files.assembly': {
                'title': 'Assembly',
                'optional': True,
                'category': 'Prediction Set Details',
                'description': 'The assembly associated with the prediction set.'
            },
            'files.transcriptome_annotation': {
                'title': 'Transcriptome Annotation',
                'optional': True,
                'category': 'Prediction Set Details',
                'description': 'The transcriptome annotation version of the analysis.'
            },
            'files.content_type': {
                'title': 'File Type',
                'category': 'File',
                'description': 'The type of files included in the measurement set.'
            },
            'files.file_format': {
                'title': 'File Format',
                'optional': True,
                'category': 'File',
                'description': 'The file formats included in the measurement set.'
            },
            'controlled_access': {
                'title': 'Controlled Access',
                'optional': True,
                'category': 'File',
                'description': 'Boolean value indicating whether access to the data is restricted.'
            },
            'data_use_limitation_summaries': {
                'title': 'Data Use Limitation',
                'optional': True,
                'category': 'File',
                'description': 'Summaries of restrictions or limitations on data usage.'
            },
            'collections': {
                'title': 'Collections',
                'optional': True,
                'category': 'Provenance',
                'description': 'Data collections the measurement set is a part of.'
            },
            'lab.title': {
                'title': 'Lab',
                'category': 'Provenance',
                'description': 'Lab that generated or submitted the data.'
            },
            'award.component': {
                'title': 'Award',
                'optional': True,
                'category': 'Provenance',
                'description': 'Grant associated with the data.'
            },
            'release_timestamp': {
                'title': 'Release Date',
                'optional': True,
                'category': 'Provenance',
                'description': 'The date the measurement set was publicly released.'
            },
            'creation_timestamp': {
                'title': 'Creation Date',
                'optional': True,
                'category': 'Provenance',
                'description': 'The date the measurement set was submitted.'
            },
            'status': {
                'title': 'Status',
                'category': 'Quality',
                'description': 'The status of the analysis.'
            },
            'audit.ERROR.category': {
                'title': 'Audit Category: Error',
                'optional': True,
                'category': 'Quality',
                'description': 'Audit for errors: identifies incorrect or inconsistent metadata. Datasets flagged cannot be released until resolved.'
            },
            'audit.NOT_COMPLIANT.category': {
                'title': 'Audit Category: Not Compliant',
                'optional': True,
                'category': 'Quality',
                'description': 'Audit for non-compliance: identifies data that does not meet compliance standards. Release requires special approval.'
            },
            'audit.WARNING.category': {
                'title': 'Audit Category: Warning',
                'optional': True,
                'category': 'Quality',
                'description': 'Audit for warnings: flags potentially inconsistent metadata. Datasets may be released despite warnings.'
            },
            'audit.INTERNAL_ACTION.category': {
                'title': 'Audit Category: Internal Action',
                'optional': True,
                'category': 'Quality',
                'description': 'Audit for internal action: identifies metadata issues requiring DACC staff resolution.'
            },
            'type': {
                'title': 'Object Type',
                'optional': True,
                'category': 'Quality',
                'description': 'The object type of the item.'
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
