from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='ConstructLibrary'
)
def construct_library():
    return {
        'facets': {
            'award.component': {
                'title': 'Award'
            },
            'lab.title': {
                'title': 'Lab'
            },
            'scope': {
                'title': 'Scope'
            },
            'selection_criteria': {
                'title': 'Selection Criteria'
            },
            'collections': {
                'title': 'Collections',
            },
            'status': {
                'title': 'Status'
            }
        },
        'facet_groups': [
            {
                'title': 'File Set',
                'facet_fields': [
                    'selection_criteria',
                    'scope',
                ],
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'collections',
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
            'aliases': {
                'title': 'Aliases'
            },
            'status': {
                'title': 'Status'
            },
            'lab': {
                'title': 'Lab'
            },
            'scope': {
                'title': 'Scope'
            },
            'selection_criteria': {
                'title': 'Selection Criteria'
            },
            'guide_library_details': {
                'title': 'Guide Library Details'
            },
            'reporter_library_details': {
                'title': 'Reporter Library Details'
            },
            'expression_vector_library_details': {
                'title': 'Expression Vector Library Details'
            },
        }
    }
