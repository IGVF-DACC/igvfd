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
            },
            'type': {
                'title': 'Object Type',
            },
            'audit.ERROR.category': {
                'title': 'Audit Category: Error'
            },
            'audit.NOT_COMPLIANT.category': {
                'title': 'Audit Category: Not Compliant'
            },
            'audit.WARNING.category': {
                'title': 'Audit Category: Warning'
            },
            'audit.INTERNAL_ACTION.category': {
                'title': 'Audit Category: Internal Action'
            },
        },
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
