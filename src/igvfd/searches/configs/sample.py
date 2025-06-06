from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Sample'
)
def sample():
    return {
        'facets': {
            'taxa': {
                'title': 'Taxa',
            },
            'sex': {
                'title': 'Sex',
            },
            'classifications': {
                'title': 'Classification',
            },
            'sample_terms.term_name': {
                'title': 'Sample'
            },
            'disease_terms.term_name': {
                'title': 'Disease'
            },
            'biosample_qualifiers': {
                'title': 'Biosample Qualifier',
            },
            'targeted_sample_term.term_name': {
                'title': 'Cellular Transformation Target',
            },
            'growth_medium': {
                'title': 'Growth Medium',
            },
            'multiplexing_methods': {
                'title': 'Multiplexing Method',
            },
            'preservation_method': {
                'title': 'Preservation Method',
            },
            'embryonic': {
                'title': 'Embryonic',
            },
            'virtual': {
                'title': 'Virtual'
            },
            'donors.ethnicities': {
                'title': 'Ethnicity',
            },
            'donors.strain': {
                'title': 'Strain'
            },
            'file_sets.file_set_type': {
                'title': 'File Set Type'
            },
            'file_sets.preferred_assay_title': {
                'title': 'Assay Title'
            },
            'construct_library_sets.file_set_type': {
                'title': 'Library Type'
            },
            'construct_library_sets.associated_phenotypes.term_name': {
                'title': 'Associated Phenotype'
            },
            'nucleic_acid_delivery': {
                'title': 'Nucleic Acid Delivery Method'
            },
            'biomarkers.name_quantification': {
                'title': 'Biomarker'
            },
            'biomarkers.classification': {
                'title': 'Biomarker Classification'
            },
            'biomarkers.gene.symbol': {
                'title': 'Biomarker Gene'
            },
            'treatments.depletion': {
                'title': 'Depletion'
            },
            'treatments.purpose': {
                'title': 'Treatment Purpose'
            },
            'treatments.treatment_type': {
                'title': 'Treatment Type'
            },
            'treatments.treatment_term_name': {
                'title': 'Treatment Name'
            },
            'modifications.cas': {
                'title': 'Cas'
            },
            'modifications.cas_species': {
                'title': 'Cas Species'
            },
            'modifications.fused_domain': {
                'title': 'Fused Domain'
            },
            'modifications.modality': {
                'title': 'Modality'
            },
            'modifications.degron_system': {
                'title': 'Degron System'
            },
            'modifications.tagged_proteins.symbol': {
                'title': 'Tagged Protein'
            },
            'collections': {
                'title': 'Collection',
            },
            'institutional_certificates.controlled_access': {
                'title': 'Controlled Access',
            },
            'institutional_certificates.data_use_limitation_summary': {
                'title': 'Data Use Limitation',
            },
            'lab.title': {
                'title': 'Lab',
            },
            'award.component': {
                'title': 'Award',
            },
            'status': {
                'title': 'Status'
            },
            'type': {
                'title': 'Object Type'
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
        },
    }


@search_config(
    name='sample-cell-lines'
)
def sample_cell_lines():
    return {
        'matrix': {
            'x': {
                'group_by': 'file_sets.preferred_assay_title',
                'label': 'Assays'
            },
            'y': {
                'group_by': ['sample_terms.term_name', 'sex'],
                'label': 'Samples'
            }
        }
    }


@search_config(
    name='sample-differentiated-specimens'
)
def sample_differentiated_specimens():
    return {
        'matrix': {
            'x': {
                'group_by': 'file_sets.preferred_assay_title',
                'label': 'Assays'
            },
            'y': {
                'group_by': ['targeted_sample_term.term_name', 'sex'],
                'label': 'Cellular Transformation Target'
            }
        }
    }
