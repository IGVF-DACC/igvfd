from snovault import upgrade_step


@upgrade_step('tissue', '1', '2')
def tissue_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-207
    return
