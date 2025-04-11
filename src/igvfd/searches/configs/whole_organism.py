from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='WholeOrganism'
)
def whole_organism():
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
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'accession': {
                'title': 'Accession'
            },
            'sample_terms': {
                'title': 'Sample Terms'
            },
            'alternate_accessions': {
                'title': 'Alternate Accessions'
            },
            'classifications': {
                'title': 'Classifications'
            },
            'donors': {
                'title': 'Donors'
            },
            'date_obtained': {
                'title': 'Date Obtained'
            },
            'taxa': {
                'title': 'Taxa'
            },
            'institutional_certificates': {
                'title': 'Institutional Certificates'
            },
            'award': {
                'title': 'Award'
            },
            'lab': {
                'title': 'Lab'
            },
            'status': {
                'title': 'Status'
            },
            'summary': {
                'title': 'Summary'
            },
            'virtual': {
                'title': 'Virtual'
            },
            'description': {
                'title': 'Description'
            }
        }
    }
