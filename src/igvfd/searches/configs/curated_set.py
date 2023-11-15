from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='CuratedSet'
)
def curated_set():
    return {
        'facets': {
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
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
            'collections': {
                'title': 'Collections'
            },
            'file_set_type': {
                'title': 'File Set Type'
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
                'title': 'File Set',
                'facet_fields': [
                    'taxa',
                    'file_set_type',
                    'assemblies',
                    'transcriptome_annotations',
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
