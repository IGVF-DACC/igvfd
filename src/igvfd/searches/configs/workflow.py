from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='Workflow'
)
def workflow():
    return {
        'facets': {
            'uniform_pipeline': {
                'title': 'Uniform Pipeline'
            },
            'analysis_steps.analysis_step_versions.software_versions.software.title': {
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
        'columns': {
            'accession': {
                'title': 'Accession'
            },
            'alternate_accessions': {
                'title': 'Alternate Accessions'
            },
            'uniform_pipeline': {
                'title': 'Uniform Pipeline'
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
