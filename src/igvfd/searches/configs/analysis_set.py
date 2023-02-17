from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='AnalysisSet'
)
def analysis_set():
    return {
        'facets': {
            'collections': {
                'title': 'Collections',
            },
            'donors.taxa': {
                'title': 'Donor Taxa',
            },
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
        'facet_groups': [
            {
                'title': 'Sample',
                'facet_fields': [
                    'collections',
                    'donors.taxa',
                ],
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'lab.title',
                    'award.component',
                ],
            },
            {
                'title': 'Quality',
                'facet_fields': [
                    'status',
                ],
            },
        ],
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
            'donors.taxa': {
                'title': 'Donor Taxa'
            },
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award'
            },
            'input_file_sets': {
                'title': 'Input File Sets'
            },
            'summary': {
                'title': 'Summary'
            }
        },
    }
