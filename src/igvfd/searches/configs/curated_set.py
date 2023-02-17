from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='CuratedSet'
)
def curated_set():
    return {
        'facets': {
            'status': {
                'title': 'Status'
            },
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
            'curated_set_type': {
                'title': 'Curated Set Type'
            },
        },
        'facet_groups': [
            {
                'title': 'Sample',
                'facet_fields': [
                    'taxa',
                    'collections',
                    'curated_set_type',
                ],
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'lab.title',
                    'award.component',
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
            'uuid': {
                'title': 'UUID'
            },
            'aliases': {
                'title': 'Aliases'
            },
            'status': {
                'title': 'Status'
            },
            'sample': {
                'title': 'Sample'
            },
            'donor': {
                'title': 'Donor'
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
            'curated_set_type': {
                'title': 'Curated Set Type'
            },
            'summary': {
                'title': 'Summary'
            }
        }
    }
