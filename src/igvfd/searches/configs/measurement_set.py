from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='MeasurementSet'
)
def measurement_set():
    return {
        'facets': {
            'assay_term.term_name': {
                'title': 'Assay'
            },
            'preferred_assay_title': {
                'title': 'Preferred Assay Title'
            },
            'control_type': {
                'title': 'Control Type'
            },
            'functional_assay_mechanisms.term_name': {
                'title': 'Measured Mechanisms'
            },
            'auxiliary_sets.file_set_type': {
                'title': 'Auxiliary Data'
            },
            'samples.construct_library_sets.file_set_type': {
                'title': 'Construct Library Data'
            },
            'samples.construct_library_sets.small_scale_gene_list.symbol': {
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
            'collections': {
                'title': 'Collections',
            },
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award'
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
                'title': 'Exteernally Hosted'
            },
            'type': {
                'title': 'Object Type',
            },
        },
        'facet_groups': [
            {
                'title': 'Measurement Set Details',
                'facet_fields': [
                    'assay_term.term_name',
                    'preferred_assay_title',
                    'control_type',
                    'functional_assay_mechanisms.term_name',
                    'auxiliary_sets.file_set_type',
                    'samples.construct_library_sets.file_set_type',
                    'targeted_genes.symbol',
                    'samples.construct_library_sets.small_scale_gene_list.symbol',
                    'files.sequencing_platform.term_name',
                ],
            },
            {
                'title': 'Sample',
                'facet_fields': [
                    'donors.taxa',
                    'samples.classifications',
                    'samples.sample_terms.term_name',
                    'samples.targeted_sample_term.term_name',
                    'samples.disease_terms.term_name',
                    'samples.modifications.modality',
                    'samples.treatments.treatment_term_name',
                    'sequencing_library_types',
                ],
            },
            {
                'title': 'Files',
                'facet_fields': [
                    'files.content_type',
                    'files.file_format'
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
                    'audit.INTERNAL_ACTION.category',
                    'externally_hosted',
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
            'functional_assay_mechanisms.term_name': {
                'title': 'Functional Assay Mechanisms'
            }
        }
    }
