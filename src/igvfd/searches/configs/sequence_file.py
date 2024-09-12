from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='SequenceFile'
)
def sequence_file():
    return {
        'facets': {
            'file_format': {
                'title': 'File Format'
            },
            'content_type': {
                'title': 'Content Type'
            },
            'illumina_read_type': {
                'title': 'Illumina Read Type'
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
            'file_set.samples.term_name': {
                'title': 'Sample Term'
            },
            'file_set.samples.classifications': {
                'title': 'Sample Classification'
            },
            'file_set.samples.disease_terms.term_name': {
                'title': 'Sample Phenotype'
            },
            'collections': {
                'title': 'Collections'
            },
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award',
            },
            'upload_status': {
                'title': 'Upload Status'
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
                'title': 'Format',
                'facet_fields': [
                    'file_format',
                    'content_type',
                    'illumina_read_type',
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
                    'file_set.samples.term_name',
                    'file_set.samples.classifications',
                    'file_set.samples.disease_terms.term_name',
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
                    'upload_status',
                    'status',
                    'audit.ERROR.category',
                    'audit.NOT_COMPLIANT.category',
                    'audit.WARNING.category',
                    'audit.INTERNAL_ACTION.category',
                ],
            },
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
            'content_type': {
                'title': 'Content Type'
            },
            'file_format': {
                'title': 'File Format'
            },
            'lab': {
                'title': 'Lab'
            },
            'status': {
                'title': 'Status'
            },
            'file_set': {
                'title': 'File Set'
            },
            'illumina_read_type': {
                'title': 'Illumina Read Type'
            },
            'dbxrefs': {
                'title': 'External Identifiers'
            },
            'upload_status': {
                'title': 'Upload Status'
            }
        }
    }
