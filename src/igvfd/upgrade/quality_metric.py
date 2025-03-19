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
