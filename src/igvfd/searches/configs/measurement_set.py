from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='MeasurementSet'
)
def measurement_set():
    return {
        'facets': {
            'donors.taxa': {
                'title': 'Taxa',
            },
            'assay_term.term_name': {
                'title': 'Assay Term'
            },
            'collections': {
                'title': 'Collections',
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
        },
        'facet_groups': [
            {
                'title': 'File Set',
                'facet_fields': [
                    'donors.taxa',
                    'assay_term.term_name',
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
            'alternate_accessions': {
                'title': 'Alternate Accessions'
            },
            'uuid': {
                'title': 'UUID'
            },
            'aliases': {
                'title': 'Aliases'
            },
            'status': {
                'title': 'Status'
            },
            'samples': {
                'title': 'Samples'
            },
            'donors': {
                'title': 'Donors'
            },
            'lab': {
                'title': 'Lab'
            },
            'award': {
                'title': 'Award'
            },
            'assay_term': {
                'title': 'Assay Term'
            },
            'protocol': {
                'title': 'Protocol'
            },
            'summary': {
                'title': 'Summary'
            },
            'donors.taxa': {
                'title': 'Taxa'
            }
        }
    }
