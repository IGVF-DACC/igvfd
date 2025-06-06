import pytest


def test_single_cell_rna_seq_quality_metric_upgrade_1_2(upgrader, single_cell_rna_seq_quality_metric_v1):
    value = upgrader.upgrade('single_cell_rna_seq_quality_metric',
                             single_cell_rna_seq_quality_metric_v1, current_version='1', target_version='2')
    assert 'frac_dup' not in value
    assert 'frac_mito' not in value
    assert 'frac_mito_genes' not in value
    assert 'frac_reads_in_genes_barcode' not in value
    assert 'frac_reads_in_genes_library' not in value
    assert 'joint_barcodes_passing' not in value
    assert 'median_genes_per_barcode' not in value
    assert 'n_genes' not in value
    assert 'pct_duplicates' not in value
    assert 'numBarcodesOnOnlist' not in value
    assert 'percentageBarcodesOnOnlist' not in value
    assert 'numReadsOnOnlist' not in value
    assert 'percentageReadsOnOnlist' not in value
    assert 'k-mer length' not in value
    assert 'num_barcodes_on_onlist' in value
    assert 'percentage_barcodes_on_onlist' in value
    assert 'num_reads_on_onlist' in value
    assert 'percentage_reads_on_onlist' in value
    assert 'kmer_length' in value
    assert value['schema_version'] == '2'
