from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='subfacets'
)
def subfacets():
    return {
        'facets': {
            'samples.classifications': {
                'title': 'Classification',
                'type': 'hierarchical',
                'subfacets': [
                    {
                        'field': 'samples.sample_terms.term_name',
                        'title': 'Sample term name',
                    },
                ]
            },
            'preferred_assay_title': {
                'title': 'Preferred Assay Title',
                'type': 'hierarchical',
                'subfacets': [
                    {
                        'field': 'lab.title',
                        'title': 'Lab title',
                    },
                    {
                        'field': 'status',
                        'title': 'Status',
                    },
                ]
            },
            'assay_term.term_name': {
                'title': 'Assay',
                'type': 'hierarchical',
                'subfacets': [
                    {
                        'field': 'samples.classifications',
                        'title': 'Classification',
                    }
                ]
            },
            'donors.taxa': {
                'title': 'Donors',
                'type': 'hierarchical',
                'subfacets': [
                    {
                        'field': 'assay_term.term_name',
                        'title': 'Assay',
                    },
                    {
                        'field': 'preferred_assay_title',
                        'title': 'Preferred assay title',
                    },
                ]

            }
        }
    }


@search_config(
    name='subfacets-types'
)
def subfacet_types():
    return {
        'facets': {
            'type': {
                'title': 'Data type',
                'type': 'hierarchical',
                'subfacets': [
                    {
                        'field': 'type',
                        'title': 'Data type',
                    }
                ]
            }
        }
    }
