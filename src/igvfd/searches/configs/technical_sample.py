from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='TechnicalSample'
)
def technical_sample():
    return {
        'facets': {
            'taxa': {
                'title': 'Taxa',
            },
            'classifications': {
                'title': 'Classification',
            },
            'sample_material': {
                'title': 'Sample Material',
            },
            'sample_terms.term_name': {
                'title': 'Sample'
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
            'nucleic_acid_delivery': {
                'title': 'Nucleic Acid Delivery Method'
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
                'title': 'Classifications',
            },
            'date_obtained': {
                'title': 'Date Obtained'
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
            'description': {
                'title': 'Description'
            },
            'summary': {
                'title': 'Summary'
            },
            'virtual': {
                'title': 'Virtual'
            }
        }
    }
