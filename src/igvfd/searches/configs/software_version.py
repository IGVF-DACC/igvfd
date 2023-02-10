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
        }
    }
