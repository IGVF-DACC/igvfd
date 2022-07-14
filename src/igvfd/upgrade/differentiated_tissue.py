from snovault import upgrade_step


@upgrade_step('differentiated_tissue', '2', '3')
def differentiated_tissue_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-210
    return


@upgrade_step('differentiated_tissue', '1', '2')
def differentiated_tissue_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-207
    return
