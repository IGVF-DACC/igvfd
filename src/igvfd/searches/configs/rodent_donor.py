from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='RodentDonor'
)
def rodent_donor():
    return {
        'facets': {
            'strain_background': {
                'title': 'Strain Background',
            },
            'sex': {
                'title': 'Sex'
            },
            'collections': {
                'title': 'Collections',
            },
            'lab.title': {
                'title': 'Lab'
            },
            'award.component': {
                'title': 'Award',
            },
            'source.title': {
                'title': 'Source',
            },
            'status': {
                'title': 'Status'
            }
        },
        'facet_groups': [
            {
                'title': 'Donor',
                'facet_fields': [
                    'strain_background',
                    'sex',
                ],
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'collection',
                    'lab.title',
                    'award.component',
                    'source.title',
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
            'strain': {
                'title': 'Strain'
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
