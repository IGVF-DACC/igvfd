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
        'analysis_step_types': ['alignment']
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
        'analysis_step_types': ['alignment'],
    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]


@pytest.fixture
def analysis_step_3(testapp, other_lab, award):
    item = {
        'lab': other_lab['@id'],
        'award': award['@id'],
        'step_label': 'base-three-analysis-step',
        'title': 'Base Three Analysis Step',
        'input_content_types': ['reads'],
        'output_content_types': ['alignments'],
        'analysis_step_types': ['alignment'],
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
def analysis_step_v5(testapp, base_workflow):
    item = {
        'step_label': 'base-analysis-step',
        'title': 'Base Analysis Step',
        'input_content_types': ['reads', 'sequence barcodes', 'barcode onlist'],
        'output_content_types': ['alignments'],
        'analysis_step_types': ['alignment'],
        'workflow': base_workflow['@id'],
        'status': 'released'
    }
    return item


@pytest.fixture
def analysis_step_v6(testapp, base_workflow):
    item = base_workflow.copy()
    item.update({
        'input_content_types': ['reads', 'comprehensive gene count matrix'],
        'output_content_types': ['alignments', 'comprehensive gene count matrix']
    })
    return item


@pytest.fixture
def analysis_step_v8(testapp, base_workflow):
    item = {
        'schema_version': '8',
        'step_label': 'base-analysis-step',
        'title': 'Base Analysis Step',
        'input_content_types': ['reads'],
        'output_content_types': ['alignments'],
        'analysis_step_types': ['alignment'],
        'workflow': base_workflow['@id']
    }
    return item


@pytest.fixture
def analysis_step_v9(testapp, analysis_step):
    item = analysis_step.copy()
    item.update({
        'schema_version': '9',
        'input_content_types': ['biological_context'],
        'output_content_types': ['genes_genes', 'variants_genes', 'elements reference']
    })
    return item


@pytest.fixture
def analysis_step_v10(testapp, base_workflow):
    item = {
        'schema_version': '10',
        'step_label': 'base-analysis-step',
        'title': 'Base Analysis Step',
        'input_content_types': ['filtered global differential expressions', 'unfiltered global differential expression', 'unfiltered local differential expression'],
        'output_content_types': ['filtered global differential expressions', 'unfiltered global differential expression', 'unfiltered local differential expression'],
        'analysis_step_types': ['alignment'],
        'workflow': base_workflow['@id']
    }
    return item
