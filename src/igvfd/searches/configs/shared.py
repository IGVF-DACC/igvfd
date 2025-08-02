from snovault.elasticsearch.searches.configs import search_config

from igvfd.metadata.constants import FROM_FILE_FIELDS


# MeasurementSets have preferred_assay_title field.
@search_config(
    name='PreferredAssayTitleSummary'
)
def preferred_assay_title_summary():
    return {
        'matrix': {
            'y': {
                'group_by': [
                    'lab.title',
                    'preferred_assay_title',
                ],
                'label': 'Preferred assay title',
            },
            'x': {
                'group_by': 'status',
                'label': 'Status',
            }
        }
    }


# Some AnalysisSets have assay_titles field.
@search_config(
    name='AssayTitlesSummary'
)
def assay_titles_summary():
    return {
        'matrix': {
            'y': {
                'group_by': [
                    'lab.title',
                    ('assay_titles', 'no_assay_titles'),
                ],
                'label': 'Assay titles',
            },
            'x': {
                'group_by': 'status',
                'label': 'Status',
            }
        }
    }


# PredictionSets have file_set_type field.
@search_config(
    name='FileSetTypeSummary'
)
def file_set_type_summary():
    return {
        'matrix': {
            'y': {
                'group_by': [
                    'lab.title',
                    'file_set_type',
                ],
                'label': 'FileSet type',
            },
            'x': {
                'group_by': 'status',
                'label': 'Status',
            }
        }
    }


@search_config(
    name='StatusFacet'
)
def status_facet():
    return {
        'facets': {
            'status': {
                'title': 'Status',
            }
        }
    }


@search_config(
    name='from-file-fields'
)
def from_file_fields():
    columns = {
        t[1][0]: {
            'title': t[0]
        }
        for t in FROM_FILE_FIELDS
    }
    return {
        'columns': columns
    }
