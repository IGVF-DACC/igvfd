from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='TechnicalSample'
)
def technical_sample():
    return {
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'accession': {
                'title': 'Accession'
            },
            'technical_sample_term': {
                'title': 'Technical Sample Term'
            },
            'date_obtained': {
                'title': 'Date Obtained'
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
            'description': {
                'title': 'Description'
            },
        }
    }
