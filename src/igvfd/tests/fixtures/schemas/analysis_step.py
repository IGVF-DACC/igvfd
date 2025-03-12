import pytest


@pytest.fixture
def analysis_step(testapp, base_workflow, other_lab, award):
    item = {
        'lab': other_lab['@id'],
        'award': award['@id'],
        'step_label': 'base-analysis-step',
        'title': 'Base Analysis Step',
        'input_content_types': ['reads'],
        'output_content_types': ['alignments'],
        'analysis_step_types': ['alignment'],
        'workflow': base_workflow['@id']
    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]


@pytest.fixture
def analysis_step_2(testapp, base_workflow_2, other_lab, award):
    item = {
        'lab': other_lab['@id'],
        'award': award['@id'],
        'step_label': 'base-two-analysis-step',
        'title': 'Base Two Analysis Step',
        'input_content_types': ['reads'],
        'output_content_types': ['alignments'],
        'analysis_step_types': ['alignment'],
        'workflow': base_workflow_2['@id']
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


@pytest.fixture
def analysis_step_v2(testapp, base_workflow):
    item = {
        'step_label': 'base-analysis-step',
        'title': 'Base Analysis Step',
        'input_content_types': ['reads'],
        'output_content_types': ['alignments'],
        'analysis_step_types': ['alignment'],
        'workflow': base_workflow['@id']
    }
    return item


@pytest.fixture
def analysis_step_v5(testapp, analysis_step):
    item = analysis_step.copy()
    item.update({
        'schema_version': '5',
        'input_content_types': ['sequence barcodes'],
        'output_content_types': ['alignments', 'sequence barcodes', 'barcode onlist']
    })
    return item
