from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='File'
)
def file():
    return {
        'facets': {
            'award.component': {
                'title': 'Award',
            },
            'collections': {
                'title': 'Collections'
            },
            'content_type': {
                'title': 'Content Type'
            },
            'file_format': {
                'title': 'File Format'
            },
            'file_format_type': {
                'title': 'File Format Type'
            },
            'assembly': {
                'title': 'Assembly'
            },
            'transcriptome_annotation': {
                'title': 'Transcriptome Annotation'
            },
            'cell_type_annotation.term_name': {
                'title': 'Cell Type Annotation'
            },
            'file_set.file_set_type': {
                'title': 'File Set Type'
            },
            'assay_titles': {
                'title': 'Assay'
            },
            'file_set.samples.taxa': {
                'title': 'Taxa'
            },
            'file_set.samples.sample_terms.term_name': {
                'title': 'Sample Term'
            },
            'file_set.samples.classifications': {
                'title': 'Sample Classification'
            },
            'file_set.samples.disease_terms.term_name': {
                'title': 'Sample Phenotype'
            },
            'integrated_in.file_set_type': {
                'title': 'Library Type'
            },
            'integrated_in.associated_phenotypes.term_name': {
                'title': 'Associated Phenotypes'
            },
            'integrated_in.small_scale_gene_list.symbol': {
                'title': 'Construct Targeted Genes'
            },
            'lab.title': {
                'title': 'Lab'
            },
            'sequencing_kit': {
                'title': 'Sequencing Kit'
            },
            'sequencing_platform.term_name': {
                'title': 'Sequencing Platform'
            },
            'status': {
                'title': 'Status'
            },
            'upload_status': {
                'title': 'Upload Status'
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
                'title': 'Format',
                'facet_fields': [
                    'file_format',
                    'file_format_type',
                    'content_type',
                ],
            },
            {
                'title': 'File Set',
                'facet_fields': [
                    'file_set.file_set_type',
                    'assay_titles',
                ],
            },
            {
                'title': 'Sample',
                'facet_fields': [
                    'file_set.samples.taxa',
                    'file_set.samples.sample_terms.term_name',
                    'file_set.samples.classifications',
                    'file_set.samples.disease_terms.term_name',
                    'cell_type_annotation.term_name',
                ],
            },
            {
                'title': 'Construct Design Data',
                'facet_fields': [
                    'integrated_in.file_set_type',
                    'integrated_in.associated_phenotypes.term_name',
                    'integrated_in.small_scale_gene_list.symbol',
                ],
            },
            {
                'title': 'Assembly',
                'facet_fields': [
                    'assembly',
                    'transcriptome_annotation',
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
                'title': 'Sequencing Method',
                'facet_fields': [
                    'sequencing_platform.term_name',
                    'sequencing_kit',
                ],
            },
            {
                'title': 'Quality',
                'facet_fields': [
                    'upload_status',
                    'status',
                    'audit.ERROR.category',
                    'audit.NOT_COMPLIANT.category',
                    'audit.WARNING.category',
                    'audit.INTERNAL_ACTION.category',
                ],
            },
        ]
    }
