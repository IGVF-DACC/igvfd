from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='MeasurementSet'
)
def measurement_set():
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
            'assay_term': {
                'title': 'Assay Term'
            },
            'protocol': {
                'title': 'Protocol'
            },
        },
        'columns': {
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
            'assay_term': {
                'title': 'Assay Term'
            },
            'protocol': {
                'title': 'Protocol'
            },
        }
    }
