from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Donor'
)
def donor():
    return {
        'facets': {
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
            },
            'type': {
                'title': 'Object Type',
            },
        },
        'facet_groups': [
            {
                'title': 'Donor',
                'facet_fields': [
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
                    'type',
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
            'alternate_accessions': {
                'title': 'Alternate Accessions'
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
