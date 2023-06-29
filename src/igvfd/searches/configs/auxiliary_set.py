from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='AuxiliarySet'
)
def auxiliary_set():
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
            'auxiliary_type': {
                'title': 'Auxiliary Type'
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
            'auxiliary_type': {
                'title': 'Auxiliary Type'
            },
            'samples': {
                'title': 'Samples'
            },
            'donors': {
                'title': 'Donors'
            },
        }

    }
