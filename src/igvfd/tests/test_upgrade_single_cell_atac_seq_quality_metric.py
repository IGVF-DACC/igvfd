import pytest


def test_single_cell_atac_seq_quality_metric_upgrade_1_2(upgrader, single_cell_atac_seq_quality_metric_v1):
    value = upgrader.upgrade('single_cell_atac_seq_quality_metric',
                             single_cell_atac_seq_quality_metric_v1, current_version='1', target_version='2')
    assert 'n_fragment' not in value
    assert 'frac_dup' not in value
    assert 'frac_mito' not in value
    assert 'tsse' not in value
    assert 'duplicate' not in value
    assert 'unmapped' not in value
    assert 'lowmapq' not in value
    assert value['schema_version'] == '2'


def test_single_cell_atac_seq_quality_metric_upgrade_2_3(upgrader, single_cell_atac_seq_quality_metric_v2):
    value = upgrader.upgrade('single_cell_atac_seq_quality_metric',
                             single_cell_atac_seq_quality_metric_v1, current_version='2', target_version='3')
    assert 'joint_barcodes_passing' not in value
    assert 'n_barcodes' not in value
    assert 'n_fragments' not in value
    assert value['schema_version'] == '3'
