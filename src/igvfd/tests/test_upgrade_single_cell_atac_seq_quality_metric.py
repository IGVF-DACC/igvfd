import pytest


def test_mpra_quality_metric_upgrade_1_2(upgrader, mpra_quality_metric_v1):
    value = upgrader.upgrade('mpra_quality_metric', mpra_quality_metric_v1, current_version='1', target_version='2')
    assert 'pct_oligos_passing' not in value
    assert value['fraction_oligos_passing'] == 0.5
    assert 'median_assigned_barocdes' not in value
    assert value['median_assigned_barcodes'] == 16
    assert value['schema_version'] == '2'


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
