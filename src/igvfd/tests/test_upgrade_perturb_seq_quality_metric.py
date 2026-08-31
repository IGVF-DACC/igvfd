def test_perturb_seq_quality_metric_upgrade_1_2(upgrader, perturb_seq_quality_metric_v1):
    value = upgrader.upgrade(
        'perturb_seq_quality_metric',
        perturb_seq_quality_metric_v1,
        current_version='1',
        target_version='2',
    )
    assert 'pct_cells_assigned_guide' not in value
    assert value['frac_cells_with_guide'] == 0.8
    assert 'avg_cells_per_target' not in value
    assert value['avg_cells_per_guide'] == 12
    assert 'mean_mitochondrial_reads' not in value
    assert value['mean_percent_mitochondrial'] == 5.5
    assert 'total_targets' not in value
    assert 'guide_diversity' not in value
    assert value['schema_version'] == '2'
