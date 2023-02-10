from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='AccessKey'
)
def access_key():
    return {
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'status': {
                'title': 'Status'
            },
            'access_key_id': {
                'title': 'Access Key ID'
            }
        }
    }
