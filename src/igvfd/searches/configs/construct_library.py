from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='ConstructLibrary'
)
def cell_line():
    return {
        'facets': {
            'status': {
                'title': 'Status'
            },
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
            }
        },
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
            }
        }

    }
