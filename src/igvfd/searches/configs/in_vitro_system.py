from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='InVitroSystem'
)
def in_vitro_system():
    return {
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'accession': {
                'title': 'Accession'
            },
            'classification': {
                'title': 'Classification'
            },
            'biosample_term': {
                'title': 'Biosample Term'
            },
            'donors': {
                'title': 'Donors'
            },
            'originated_from': {
                'title': 'Originated From'
            },
            'taxa': {
                'title': 'Taxa'
            },
            'award': {
                'title': 'Award'
            },
            'lab': {
                'title': 'Lab'
            },
            'status': {
                'title': 'Status'
            },
            'submitted_by': {
                'title': 'Submitted By'
            },
        }
    }
