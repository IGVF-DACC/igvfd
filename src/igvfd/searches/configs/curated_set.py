from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='CuratedSet'
)
def curated_set():
    return {
        'facets': {
            'file_set_type': {
                'title': 'File Set Type'
            },
            'assemblies': {
                'title': 'Assemblies'
            },
            'transcriptome_annotations': {
                'title': 'Transcriptome Annotations'
            },
            'taxa': {
                'title': 'Taxa'
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
                'title': 'Modification',
            },
            'samples.treatments.treatment_term_name': {
                'title': 'Treatment',
            },
            'files.content_type': {
                'title': 'File Type',
            },
            'files.file_format': {
                'title': 'File Format',
            },
            'collections': {
                'title': 'Collections'
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
            'type': {
                'title': 'Object Type'
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
            'description': {
                'title': 'Description'
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
            'taxa': {
                'title': 'Taxa'
            },
            'assemblies': {
                'title': 'Assemblies'
            },
            'transcriptome_annotations': {
                'title': 'Transcriptome Annotations'
            },
            'file_set_type': {
                'title': 'File Set Type'
            },
            'summary': {
                'title': 'Summary'
            }
        }
    }
