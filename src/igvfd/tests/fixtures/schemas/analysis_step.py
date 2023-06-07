import pytest


@pytest.fixture
def analysis_step(testapp):
    item = {
        'step_label': 'base-analysis-step',
        'title': 'Base Analysis Step',
        'major_version': 1,
        'input_content_types': ['reads'],
        'analysis_step_types': ['alignment'],

    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]
