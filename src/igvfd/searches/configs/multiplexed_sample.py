from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='MultiplexedSample'
)
def multiplexed_sample():
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
                'title': 'Sample Term'
            },
            'disease_terms.term_name': {
                'title': 'Disease Term'
            },
            'multiplexing_method': {
                'title': 'Multiplexing Method',
            },
            'embryonic': {
                'title': 'Embryonic',
            },
            'virtual': {
                'title': 'Virtual'
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
            'construct_library_sets.nucleic_acid_delivery': {
                'title': 'Delivery'
            },
            'biomarkers.name': {
                'title': 'Biomarker'
            },
            'biomarkers.classification': {
                'title': 'Biomarker Classification'
            },
            'biomarkers.quantification': {
                'title': 'Biomarker Quantification'
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
                'title': 'Treatment Term Name'
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
            'modifications.tagged_protein.symbol': {
                'title': 'CRISPR Tagged Protein'
            },
            'modifications.degron_system': {
                'title': 'Degron System'
            },
            'modifications.tagged_proteins.symbol': {
                'title': 'Degron Tagged Protein'
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
        'facet_groups': [
            {
                'title': 'Sample',
                'facet_fields': [
                    'taxa',
                    'classifications',
                    'sample_terms.term_name',
                    'disease_terms.term_name',
                    'multiplexing_method',
                    'embryonic',
                    'virtual',
                ]
            },
            {
                'title': 'File Set',
                'facet_fields': [
                    'file_sets.preferred_assay_title',
                    'file_sets.file_set_type',
                ]
            },
            {
                'title': 'Construct Library',
                'facet_fields': [
                    'construct_library_sets.file_set_type',
                    'construct_library_sets.associated_phenotypes.term_name',
                    'nucleic_acid_delivery',
                ]
            },
            {
                'title': 'Treatment',
                'facet_fields': [
                    'treatments.treatment_type',
                    'treatments.treatment_term_name',
                    'treatments.purpose',
                    'treatments.depletion',
                ]
            },
            {
                'title': 'Biomarker',
                'facet_fields': [
                    'biomarkers.name',
                    'biomarkers.classification',
                    'biomarkers.quantification',
                    'biomarkers.gene.symbol',
                ]
            },
            {
                'title': 'Modification',
                'facet_fields': [
                    'modifications.modality',
                    'modifications.cas',
                    'modifications.cas_species',
                    'modifications.fused_domain',
                    'modifications.tagged_protein.symbol',
                    'modifications.degron_system',
                    'modifications.tagged_proteins.symbol',
                ]
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'collections',
                    'lab.title',
                    'award.component',
                    'type',
                ]
            },
            {
                'title': 'Quality',
                'facet_fields': [
                    'status',
                    'audit.ERROR.category',
                    'audit.NOT_COMPLIANT.category',
                    'audit.WARNING.category',
                    'audit.INTERNAL_ACTION.category',
                ]
            }
        ],
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'accession': {
                'title': 'Accession'
            },
            'alternate_accessions': {
                'title': 'Alternate Accessions'
            },
            'classifications': {
                'title': 'Classifications',
            },
            'sample_terms': {
                'title': 'Sample Terms'
            },
            'donors': {
                'title': 'Donors'
            },
            'date_obtained': {
                'title': 'Date Obtained'
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
