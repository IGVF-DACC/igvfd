from snovault import upgrade_step


@upgrade_step('tissue', '2', '3')
def tissue_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-210
    return


@upgrade_step('tissue', '1', '2')
def tissue_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-207
    return
