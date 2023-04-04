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
        },
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
