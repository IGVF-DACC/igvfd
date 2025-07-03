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
                ]
            },
            'preferred_assay_titles': {
                'title': 'Preferred Assay Titles'
            },
            'control_types': {
                'title': 'Control Types'
            },
            'functional_assay_mechanisms.term_name': {
                'title': 'Measured Mechanisms'
            },
            'auxiliary_sets.file_set_type': {
                'title': 'Auxiliary Data'
            },
            'construct_library_sets.file_set_type': {
                'title': 'Construct Library Data'
            },
            'construct_library_sets.small_scale_gene_list.symbol': {
                'title': 'Investigated Gene'
            },
            'targeted_genes.symbol': {
                'title': 'Readout Genes'
            },
            'files.sequencing_platform.term_name': {
                'title': 'Sequencing Platform'
            },
            'donors.taxa': {
                'title': 'Taxa',
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
            'samples.modifications.modality': {
                'title': 'Modification'
            },
            'samples.treatments.treatment_term_name': {
                'title': 'Treatment'
            },
            'sequencing_library_types': {
                'title': 'Library Material'
            },
            'files.content_type': {
                'title': 'File Types',
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
            'externally_hosted': {
                'title': 'Externally Hosted'
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
                'title': 'Assay'
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
            'title': 'Assay'
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
                'group_by': ['assay_term.assay_slims', 'assay_term.term_name', 'preferred_assay_title'],
                'label': 'Samples'
            }
        }
    }
