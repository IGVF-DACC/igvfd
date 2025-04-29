from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='AnalysisStepVersion'
)
def analysis_step_version():
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
            }
        },
        'columns': {
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
            'title': {
                'title': 'Title'
            },
            'summary': {
                'title': 'Summary'
            },
            'software_versions': {
                'title': 'Software Versions'
            },
            'analysis_step': {
                'title': 'Analysis Step'
            },
            'analysis_step.title': {
                'title': 'Analysis Step Title'
            }
        }
    }
