import pytest


@pytest.fixture
def analysis_step(testapp, other_lab, award):
    item = {
        'lab': other_lab['@id'],
        'award': award['@id'],
        'step_label': 'base-analysis-step',
        'title': 'Base Analysis Step',
        'input_content_types': ['reads'],
        'output_content_types': ['alignments'],
        'analysis_step_types': ['alignment'],
    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]


@pytest.fixture
def analysis_step_2(testapp, other_lab, award):
    item = {
        'lab': other_lab['@id'],
        'award': award['@id'],
        'step_label': 'base-two-analysis-step',
        'title': 'Base Two Analysis Step',
        'input_content_types': ['reads'],
        'output_content_types': ['alignments'],
        'analysis_step_types': ['alignment']
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
def analysis_step_v2(testapp):
    item = {
        'step_label': 'base-analysis-step',
        'title': 'Base Analysis Step',
        'input_content_types': ['reads'],
        'output_content_types': ['alignments'],
        'analysis_step_types': ['alignment']
    }
    return item


@pytest.fixture
def analysis_step_v5(testapp):
    item = {
        'step_label': 'base-analysis-step',
        'title': 'Base Analysis Step',
        'input_content_types': ['reads', 'sequence barcodes', 'barcode onlist'],
        'output_content_types': ['alignments'],
        'analysis_step_types': ['alignment'],
        'status': 'released'
    }
    return item


@pytest.fixture
def analysis_step_v6(testapp, analysis_step):
    item = analysis_step.copy()
    item.update({
        'input_content_types': ['reads', 'comprehensive gene count matrix'],
        'output_content_types': ['alignments', 'comprehensive gene count matrix']
    })
    return item


@pytest.fixture
def analysis_step_v8(testapp, analysis_step, base_workflow_3):
    item = analysis_step.copy()
    item.update({'workflow': base_workflow_3['@id']})
    return item
