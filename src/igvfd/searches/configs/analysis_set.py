from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='AnalysisSet'
)
def analysis_set():
    return {
        'facets': {
            'collections': {
                'title': 'Collections',
            },
            'donors.taxa': {
                'title': 'Taxa',
            },
            'assay_titles': {
                'title': 'Assay Title'
            },
            'samples.classifications': {
                'title': 'Classification'
            },
            'samples.disease_terms.term_name': {
                'title': 'Disease',
            },
            'samples.sample_terms.term_name': {
                'title': 'Sample'
            },
            'samples.targeted_sample_term.term_name': {
                'title': 'Targeted Sample'
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
            'file_set_type': {
                'title': 'Analysis Set Type',
            },
            'files.assembly': {
                'title': 'Assembly',
            },
            'files.content_type': {
                'title': 'File Content Type',
            },
            'files.file_format': {
                'title': 'File Format',
            },
            'files.transcriptome_annotation': {
                'title': 'Transcriptome Annotation',
            },
            'workflows.uniform_pipeline': {
                'title': 'Uniformly Processed'
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
                    'samples.disease_terms.term_name'
                ],
            },
            {
                'title': 'Analysis Set Details',
                'facet_fields': [
                    'file_set_type',
                    'assay_titles',
                    'workflows.uniform_pipeline',
                    'files.assembly',
                    'files.transcriptome_annotation'
                ],
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'lab.title',
                    'award.component',
                    'collections',
                    'type',
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
                'title': 'Quality',
                'facet_fields': [
                    'status',
                    'audit.ERROR.category',
                    'audit.NOT_COMPLIANT.category',
                    'audit.WARNING.category',
                    'audit.INTERNAL_ACTION.category',
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
            'input_file_sets': {
                'title': 'Input File Sets'
            },
            'sample_summary': {
                'title': 'Sample Summary'
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
            'protocols': {
                'title': 'Protocols'
            },
            'functional_assay_mechanisms.term_name': {
                'title': 'Functional Assay Mechanisms'
            }
        },
    }
