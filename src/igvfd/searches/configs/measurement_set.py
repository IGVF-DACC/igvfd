from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='MeasurementSet'
)
def measurement_set():
    return {
        'facets': {
            'donors.taxa': {
                'title': 'Taxa',
            },
            'samples.classifications': {
                'title': 'Classifications',
            },
            'samples.sample_terms.term_name': {
                'title': 'Sample Term',
            },
            'samples.targeted_sample_term.term_name': {
                'title': 'Targeted Sample Term',
            },
            'samples.disease_terms.term_name': {
                'title': 'Disease Term',
            },
            'assay_term.term_name': {
                'title': 'Assay Term'
            },
            'preferred_assay_title': {
                'title': 'Preferred Assay Title'
            },
            'samples.modifications.modality': {
                'title': 'CRISPR Modality'
            },
            'files.sequencing_platform.term_name': {
                'title': 'Sequencing Platform'
            },
            'sequencing_library_types': {
                'title': 'Library Material'
            },
            'targeted_genes.symbol': {
                'title': 'Assay Targeted Genes'
            },
            'samples.construct_library_sets.small_scale_gene_list.symbol': {
                'title': 'Construct Library Targeted Genes'
            },
            'samples.construct_library_sets.file_set_type': {
                'title': 'Construct Library Data'
            },
            'auxiliary_sets.file_set_type': {
                'title': 'Auxiliary Data'
            },
            'files.content_type': {
                'title': 'Available File Types',
            },
            'collections': {
                'title': 'Collections',
            },
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award'
            },
            'functional_assay_mechanism.term_name': {
                'title': 'Functional Assay Mechanism'
            },
            'status': {
                'title': 'Status'
            },
            'file_set_type': {
                'title': 'File Set Type',
            },
            'type': {
                'title': 'Object Type',
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
                    'donors.taxa',
                    'samples.classifications',
                    'samples.sample_terms.term_name',
                    'samples.targeted_sample_term.term_name',
                    'samples.disease_terms.term_name',
                ],
            },
            {
                'title': 'Assay',
                'facet_fields': [
                    'assay_term.term_name',
                    'preferred_assay_title',
                    'samples.modifications.modality',
                    'file_set_type',
                    'auxiliary_sets.file_set_type',
                    'samples.construct_library_sets.file_set_type',
                    'targeted_genes.symbol',
                    'samples.construct_library_sets.small_scale_gene_list.symbol',
                    'functional_assay_mechanism.term_name'
                ],
            },
            {
                'title': 'Library',
                'facet_fields': [
                    'sequencing_library_types',
                    'files.sequencing_platform.term_name'
                ],
            },
            {
                'title': 'File Data',
                'facet_fields': [
                    'files.content_type'
                ],
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'collections',
                    'lab.title',
                    'award.component',
                    'type',
                ],
            },
            {
                'title': 'Quality',
                'facet_fields': [
                    'status',
                    'audit.ERROR.category',
                    'audit.NOT_COMPLIANT.category',
                    'audit.WARNING.category',
                    'audit.INTERNAL_ACTION.category'
                ],
            },
        ],
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
            'donors': {
                'title': 'Donors'
            },
            'lab': {
                'title': 'Lab'
            },
            'award': {
                'title': 'Award'
            },
            'assay_term': {
                'title': 'Assay Term'
            },
            'preferred_assay_title': {
                'title': 'Preferred Assay Title'
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
            'functional_assay_mechanism.term_name': {
                'title': 'Functional Assay Mechanism'
            }
        }
    }
