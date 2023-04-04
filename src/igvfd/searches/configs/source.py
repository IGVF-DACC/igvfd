from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Source'
)
def source():
    return {}
