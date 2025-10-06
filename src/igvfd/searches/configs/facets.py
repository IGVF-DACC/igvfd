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
            'preferred_assay_titles': {
                'title': 'Preferred Assay Titles',
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
                        'field': 'preferred_assay_titles',
                        'title': 'Preferred assay titles',
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


@search_config(
    name='date-histogram-release-timestamp'
)
def date_histogram_release_timestamp():
    return {
        'facets': {
            'release_timestamp': {
                'title': 'Release timestamp',
                'type': 'date_histogram',
                'calendar_interval': 'month',
                'format': 'yyyy-MM-dd',
            }
        }
    }


@search_config(
    name='range-file-size'
)
def range_file_size():
    return {
        'facets': {
            'file_size': {
                'title': 'File size',
                'type': 'range',
                'ranges': [
                    {'key': 'small', 'to': 30000000},
                    {'key': 'medium', 'from': 30000000, 'to': 50000000},
                    {'key': 'large', 'from': 50000000},
                ]
            }
        }
    }


@search_config(
    name='range-starting-amount'
)
def range_starting_amount():
    return {
        'facets': {
            'starting_amount': {
                'title': 'Starting amount',
                'type': 'range',
                'ranges': [
                    {'to': 5},
                    {'from': 5, 'to': 7},
                    {'from': 7},
                ]
            }
        }
    }
