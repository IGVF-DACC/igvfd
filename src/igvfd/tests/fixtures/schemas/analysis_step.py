import pytest


@pytest.fixture
def analysis_step(testapp, base_workflow):
    item = {
        'step_label': 'base-analysis-step',
        'title': 'Base Analysis Step',
        'input_content_types': ['reads'],
        'output_content_types': ['alignments'],
        'analysis_step_types': ['alignment'],
        'workflow': base_workflow['@id']
    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]


@pytest.fixture
def analysis_step_v1(analysis_step):
    item = analysis_step.copy()
    item.update({
        'schema_version': '1',
        'parents': [],
        'input_content_types': [],
        'output_content_types': [],
        'analysis_step_types': [],
    })
    return item
