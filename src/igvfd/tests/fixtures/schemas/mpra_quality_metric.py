import pytest


@pytest.fixture
def mpra_quality_metric(
        testapp, lab, award, alignment_file, analysis_step_version):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'quality_metric_of': alignment_file['@id'],
        'pearson_correlation': 0.82,
        'median_barcodes_passing_filtering': 900,
        'median_rna_read_count': 50,
        'fraction_oligos_passing': 0.8,
        'median_assigned_barcodes': 10,
        'fraction_assigned_oligos': 0.99,
        'analysis_step_version': analysis_step_version['@id']
    }
    return testapp.post_json('/mpra_quality_metric', item, status=201).json['@graph'][0]


@pytest.fixture
def mpra_quality_metric_v1(
        lab, award, alignment_file, analysis_step_version):
    item = {
        'schema_version': '1',
        'award': award['@id'],
        'lab': lab['@id'],
        'quality_metric_of': alignment_file['@id'],
        'pct_oligos_passing': 0.5,
        'median_assigned_barocdes': 16,
        'analysis_step_version': analysis_step_version['@id']
    }
    return item
