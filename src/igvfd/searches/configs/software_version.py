from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='SoftwareVersion'
)
def software_version():
    return {
        'facets': {
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award'
            },
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
                'title': 'Version'
            },
            'lab': {
                'title': 'Lab'
            },
        }
    }
