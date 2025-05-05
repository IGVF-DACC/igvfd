from snovault import upgrade_step


@upgrade_step('mpra_quality_metric', '1', '2')
def mpra_quality_metric_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2501
    if 'pct_oligos_passing' in value:
        value['fraction_oligos_passing'] = value['pct_oligos_passing']
        del value['pct_oligos_passing']
    if 'median_assigned_barocdes' in value:
        value['median_assigned_barcodes'] = value['median_assigned_barocdes']
        del value['median_assigned_barocdes']


@upgrade_step('single_cell_atac_seq_quality_metric', '1', '2')
def single_cell_atac_seq_quality_metric_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2566
    if 'n_fragment' in value:
        del value['n_fragment']
    if 'frac_dup' in value:
        del value['frac_dup']
    if 'frac_mito' in value:
        del value['frac_mito']
    if 'tsse' in value:
        del value['tsse']
    if 'duplicate' in value:
        del value['duplicate']
    if 'unmapped' in value:
        del value['unmapped']
    if 'lowmapq' in value:
        del value['lowmapq']


@upgrade_step('single_cell_atac_seq_quality_metric', '2', '3')
def single_cell_atac_seq_quality_metric_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2660
    if 'joint_barcodes_passing' in value:
        del value['joint_barcodes_passing']
    if 'n_barcodes' in value:
        del value['n_barcodes']
    if 'n_fragments' in value:
        del value['n_fragments']


@upgrade_step('single_cell_rna_seq_quality_metric', '1', '2')
def single_cell_rna_seq_quality_metric_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2660
    if 'frac_dup' in value:
        del value['frac_dup']
    if 'frac_mito' in value:
        del value['frac_mito']
    if 'frac_mito_genes' in value:
        del value['frac_mito_genes']
    if 'frac_reads_in_genes_barcode' in value:
        del value['frac_reads_in_genes_barcode']
    if 'frac_reads_in_genes_library' in value:
        del value['frac_reads_in_genes_library']
    if 'joint_barcodes_passing' in value:
        del value['joint_barcodes_passing']
    if 'median_genes_per_barcode' in value:
        del value['median_genes_per_barcode']
    if 'n_genes' in value:
        del value['n_genes']
    if 'pct_duplicates' in value:
        del value['pct_duplicates']
    if 'numBarcodesOnOnlist' in value:
        value['num_barcodes_on_onlist'] = value['numBarcodesOnOnlist']
        del value['numBarcodesOnOnlist']
    if 'percentageBarcodesOnOnlist' in value:
        value['percentage_barcodes_on_onlist'] = value['percentageBarcodesOnOnlist']
        del value['percentageBarcodesOnOnlist']
    if 'numReadsOnOnlist' in value:
        value['num_reads_on_onlist'] = value['numReadsOnOnlist']
        del value['numReadsOnOnlist']
    if 'percentageReadsOnOnlist' in value:
        value['percentage_reads_on_onlist'] = value['percentageReadsOnOnlist']
        del value['percentageReadsOnOnlist']
    if 'k-mer length' in value:
        value['kmer_length'] = value['k-mer length']
        del value['k-mer length']
