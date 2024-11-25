from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='DatasetSummary'
)
def dataset_summary():
    return {
        'matrix': {
            'y': {
                'group_by': [
                    'lab.title',
                    'preferred_assay_title',
                ],
                'label': 'Assay',
            },
            'x': {
                'group_by': 'status',
                'label': 'Status',
            }
        }
    }
