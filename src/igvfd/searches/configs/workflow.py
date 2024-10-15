from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Workflow'
)
def workflow():
    return {
        'facets': {
            'analysis_steps.analysis_step_versions.software_versions.software.name': {
                'title': 'Software',
            },
            'analysis_steps.analysis_step_types': {
                'title': 'Analysis Step Types',
            },
            'analysis_steps.output_content_types': {
                'title': 'Output Types',
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
                'title': 'Workflow',
                'facet_fields': [
                    'analysis_steps.analysis_step_versions.software_versions.software.name',
                    'analysis_steps.analysis_step_types',
                    'analysis_steps.output_content_types',
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
            'name': {
                'title': 'Name'
            },
            'lab': {
                'title': 'Lab'
            },
            'award': {
                'title': 'Award'
            },
            'summary': {
                'title': 'Summary'
            }
        }
    }
