from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='HumanDonor'
)
def human_donor():
    return {
        'columns': {
            'uuid': {
                'title': 'UUID'
            },
            'accession': {
                'title': 'Accession'
            },
            'aliases': {
                'title': 'Aliases'
            },
            'taxa': {
                'title': 'Taxa'
            },
            'sex': {
                'title': 'Sex'
            },
            'award': {
                'title': 'Award'
            },
            'ethnicities': {
                'title': 'Ethnicities'
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
            'collections': {
                'title': 'Collections'
            },
            'phenotypic_features': {
                'title': 'Phenotypic Features'
            }
        }
    }
