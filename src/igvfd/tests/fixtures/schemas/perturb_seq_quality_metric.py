import pytest


@pytest.fixture
def perturb_seq_quality_metric_v1(
        lab, award, alignment_file, analysis_step_version):
    item = {
        'schema_version': '1',
        'award': award['@id'],
        'lab': lab['@id'],
        'quality_metric_of': alignment_file['@id'],
        'pct_cells_assigned_guide': 0.8,
        'avg_cells_per_target': 12,
        'mean_mitochondrial_reads': 5.5,
        'total_targets': 40,
        'guide_diversity': 0.3,
        'analysis_step_version': analysis_step_version['@id']
    }
    return item
