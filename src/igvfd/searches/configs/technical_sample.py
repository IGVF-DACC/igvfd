from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='TechnicalSample'
)
def technical_sample():
    return {
        'facets': {
            'technical_sample_term.term_name': {
                'title': 'Technical Sample Term',
            },
            'collections': {
                'title': 'Collections',
            },
            'lab.title': {
                'title': 'Lab',
            },
            'award.component': {
                'title': 'Award',
            },
            'source.title': {
                'title': 'Source',
            },
            'status': {
                'title': 'Status'
            },
        },
        'facet_groups': [
            {
                'title': 'Sample',
                'facet_fields': [
                    'technical_sample_term.term_name',
                ]
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'collections',
                    'lab.title',
                    'award.component',
                    'source.title',
                ]
            },
            {
                'title': 'Quality',
                'facet_fields': [
                    'status',
                ]
            },
        ],
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'accession': {
                'title': 'Accession'
            },
            'technical_sample_term.term_name': {
                'title': 'Technical Sample Term'
            },
            'date_obtained': {
                'title': 'Date Obtained'
            },
            'award.component': {
                'title': 'Award'
            },
            'lab.title': {
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
