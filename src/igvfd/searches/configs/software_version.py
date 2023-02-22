from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='SoftwareVersion'
)
def software_version():
    return {
        'facets': {
            'status': {
                'title': 'Status'
            },
        },
        'columns': {
            'software.title': {
                'title': 'Title'
            },
            'status': {
                'title': 'Status'
            },
            'version': {
                'title': 'version'
            },
            'lab': {
                'title': 'Lab'
            },
        }
    }
