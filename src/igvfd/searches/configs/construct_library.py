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
            'award': {
                'title': 'Award'
            },
            'lab': {
                'title': 'Lab'
            },
            'scope': {
                'title': 'Scope'
            },
            'origins': {
                'title': 'Origins'
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
            'lab.title': {
                'title': 'Lab'
            },
            'scope': {
                'title': 'Scope'
            },
            'origins': {
                'title': 'Origins'
            },
            'plasmid_map': {
                'title': 'Plasmid Map'
            },
            'guide_library_details': {
                'title': 'Guide Library Details'
            },
            'reporter_library_details': {
                'title': 'Reporter Library Details'
            }
        }

    }
