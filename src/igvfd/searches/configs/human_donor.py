from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='HumanDonor'
)
def human_donor():
    return {
        'facets': {
            'ethnicities': {
                'title': 'Ethnicities'
            },
            'sex': {
                'title': 'Sex'
            },
            'collections': {
                'title': 'Collections'
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
            'virtual': {
                'title': 'Virtual'
            }
        },
        'facet_groups': [
            {
                'title': 'Donor',
                'facet_fields': [
                    'ethnicities',
                    'sex',
                    'virtual',
                ]
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'collections',
                    'lab.title',
                    'award.component',
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
            'human_donor_identifiers': {
                'title': 'Human Donor Identifiers'
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
            },
            'virtual': {
                'title': 'Virtual'
            }
        }
    }
