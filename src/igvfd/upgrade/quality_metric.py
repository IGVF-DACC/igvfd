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
