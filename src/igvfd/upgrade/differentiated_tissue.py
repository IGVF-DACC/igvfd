from snovault import upgrade_step


@upgrade_step('differentiated_tissue', '1', '2')
def differentiated_tissue_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-207
    return
