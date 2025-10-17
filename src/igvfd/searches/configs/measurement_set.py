from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='MeasurementSet'
)
def measurement_set():
    return {
        'facets': {
            'assay_term.assay_slims': {
                'title': 'Assay',
                'type': 'hierarchical',
                'subfacets': [
                    {
                        'field': 'assay_term.term_name',
                        'title': 'Assay type',
                    }
                ],
                'default': 'True'
            },
            'preferred_assay_titles': {
                'title': 'Preferred Assay Titles',
                'default': 'True'
            },
            'control_types': {
                'title': 'Control Types',
                'default': 'True'
            },
            'functional_assay_mechanisms.term_name': {
                'title': 'Measured Mechanisms',
                'default': 'False'
            },
            'auxiliary_sets.file_set_type': {
                'title': 'Auxiliary Data',
                'default': 'True'
            },
            'files.sequencing_platform.term_name': {
                'title': 'Sequencing Platform',
                'default': 'True'
            },
            'library_preparation_kit': {
                'title': 'Library Preparation Kit',
                'default': 'False'
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
                'default': 'True'
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
            'sequencing_library_types': {
                'title': 'Library Material',
                'default': 'False'
            },
            'files.content_type': {
                'title': 'File Types',
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
            'externally_hosted': {
                'title': 'Externally Hosted',
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
