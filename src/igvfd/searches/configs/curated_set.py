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
        },
        'facet_groups': [
            {
                'title': 'File Set',
                'facet_fields': [
                    'taxa',
                    'file_set_type',
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
            'file_set_type': {
                'title': 'File Set Type'
            },
            'summary': {
                'title': 'Summary'
            }
        }
    }
