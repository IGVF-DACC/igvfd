from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='ModelSet'
)
def model_set():
    return {
        'facets': {
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
            'file_set_type': {
                'title': 'File Set Type'
            },
            'prediction_objects': {
                'title': 'Prediction Objects'
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
        'facet_groups': [
            {
                'title': 'File Set',
                'facet_fields': [
                    'file_set_type',
                    'prediction_objects',
                ],
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'collections',
                    'lab.title',
                    'award.component',
                    'type',
                ],
            },
            {
                'title': 'Quality',
                'facet_fields': [
                    'status',
                    'audit.ERROR.category',
                    'audit.NOT_COMPLIANT.category',
                    'audit.WARNING.category',
                    'audit.INTERNAL_ACTION.category',
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
            'lab': {
                'title': 'Lab'
            },
            'award': {
                'title': 'Award'
            },
            'model_name': {
                'title': 'Model Name'
            },
            'file_set_type': {
                'title': 'File Set Type'
            },
            'prediction_objects': {
                'title': 'Prediction Objects'
            },
            'summary': {
                'title': 'Summary'
            }
        }
    }
