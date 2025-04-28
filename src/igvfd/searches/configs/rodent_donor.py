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
            'sources.title': {
                'title': 'Sources',
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
            },
            'virtual': {
                'title': 'Virtual'
            }
        }
    }
