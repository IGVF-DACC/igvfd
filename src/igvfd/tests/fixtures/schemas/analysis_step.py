import pytest


@pytest.fixture
def analysis_step(testapp):
    item = {
        'step_label': 'base-analysis-step',
        'title': 'Base Analysis Step',
        'input_content_types': ['reads'],
        'analysis_step_types': ['alignment'],
        'workflow': ''
    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]
