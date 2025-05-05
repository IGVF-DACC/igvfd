import pytest
from ...constants import *


@pytest.fixture
def single_cell_rna_seq_quality_metric(
        testapp, lab, award, alignment_file, analysis_step_version):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'quality_metric_of': alignment_file['@id'],
        'n_records': 50,
        'n_reads': 10,
        'n_barcodes': 0.99,
        'total_umis': 0.99,
        'n_barcode_umis': 0.99,
        'median_reads_per_barcode': 0.99,
        'mean_reads_per_barcode': 0.99,
        'median_umis_per_barcode': 0.99,
        'mean_umis_per_barcode': 0.99,
        'gt_records': 0.99,
        'numBarcodesOnOnlist': 70,
        'percentageReadsOnOnlist': 0.99,
        'n_targets': 0.99,
        'n_bootstraps': 0.99,
        'n_processed': 0.99,
        'n_pseudoaligned': 0.99,
        'n_unique': 0.99,
        'p_pseudoaligned': 0.99,
        'p_unique': 0.99,
        'index_version': 0.99,
        'k-mer length': 8,
        'rnaseq_kb_info': {'download': 'red-dot.png', 'href': RED_DOT},
        'analysis_step_version': analysis_step_version['@id']
    }
    return testapp.post_json('/single_cell_rna_seq_quality_metric', item, status=201).json['@graph'][0]


@pytest.fixture
def single_cell_rna_seq_quality_metric_v1(
        lab, award, alignment_file, analysis_step_version):
    item = {
        'schema_version': '1',
        'award': award['@id'],
        'lab': lab['@id'],
        'quality_metric_of': alignment_file['@id'],
        'n_records': 50,
        'n_reads': 10,
        'n_barcodes': 0.99,
        'frac_dup': 0.99,
        'frac_mito': 0.99,
        'frac_mito_genes': 0.99,
        'frac_reads_in_genes_barcode': 0.99,
        'frac_reads_in_genes_library': 0.99,
        'joint_barcodes_passing': 800,
        'median_genes_per_barcode': 2,
        'n_genes': 70,
        'pct_duplicates': 0.99,
        'numBarcodesOnOnlist': 800,
        'percentageBarcodesOnOnlist': 0.77,
        'numReadsOnOnlist': 800,
        'percentageReadsOnOnlist': 0.6,
        'k-mer length': 5,
        'analysis_step_version': analysis_step_version['@id']
    }
    return item
