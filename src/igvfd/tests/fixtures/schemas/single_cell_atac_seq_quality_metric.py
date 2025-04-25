import pytest
from ...constants import *


@pytest.fixture
def single_cell_atac_seq_quality_metric(
        testapp, lab, award, alignment_file, analysis_step_version):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'quality_metric_of': alignment_file['@id'],
        'n_fragments': 0.82,
        'n_barcodes': 900,
        'pct_duplicates': 50,
        'joint_barcodes_passing': 0.8,
        'n_reads': 10,
        'n_mapped_reads': 0.99,
        'n_uniquely_mapped_reads': 0.99,
        'n_reads_with_multi_mappings': 0.99,
        'n_candidates': 0.99,
        'n_mappings': 0.99,
        'n_uni_mappings': 0.99,
        'n_multi_mappings': 0.99,
        'n_barcodes_on_onlist': 0.99,
        'n_corrected_barcodes': 0.99,
        'n_output_mappings': 0.99,
        'uni_mappings': 0.99,
        'multi_mappings': 0.99,
        'total': 0.99,
        'atac_fragments_alignment_stats': {'download': 'red-dot.png', 'href': RED_DOT},
        'atac_bam_summary_stats': {'download': 'red-dot.png', 'href': RED_DOT},
        'atac_fragment_summary_stats': {'download': 'red-dot.png', 'href': RED_DOT},
        'analysis_step_version': analysis_step_version['@id']
    }
    return testapp.post_json('/single_cell_atac_seq_quality_metric', item, status=201).json['@graph'][0]


@pytest.fixture
def single_cell_atac_seq_quality_metric_v1(
        lab, award, alignment_file, analysis_step_version):
    item = {
        'schema_version': '1',
        'award': award['@id'],
        'lab': lab['@id'],
        'quality_metric_of': alignment_file['@id'],
        'n_uniquely_mapped_reads': 97820912,
        'n_barcodes': 1700,
        'n_fragment': 239056,
        'frac_dup': 0.2,
        'frac_mito': 0.11,
        'tsse': 84983,
        'duplicate': 880,
        'unmapped': 878,
        'lowmapq': 521,
        'analysis_step_version': analysis_step_version['@id']
    }
    return item


@pytest.fixture
def single_cell_atac_seq_quality_metric_v2(
        lab, award, alignment_file, analysis_step_version):
    item = {
        'schema_version': '2',
        'award': award['@id'],
        'lab': lab['@id'],
        'quality_metric_of': alignment_file['@id'],
        'n_uniquely_mapped_reads': 97820912,
        'n_barcodes': 1700,
        'n_fragments': 239056,
        'joint_barcodes_passing': 0.8,
        'frac_dup': 0.2,
        'lowmapq': 521,
        'analysis_step_version': analysis_step_version['@id']
    }
    return item
