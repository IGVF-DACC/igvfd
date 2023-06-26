import pytest


@pytest.fixture
def analysis_step(testapp, base_workflow):
    item = {
        'step_label': 'base-analysis-step',
        'title': 'Base Analysis Step',
        'input_content_types': ['reads'],
        'analysis_step_types': ['alignment'],
        'workflow': base_workflow['@id']
    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]
