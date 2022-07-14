from snovault import upgrade_step


@upgrade_step('cell_line', '2', '3')
def cell_line_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-210
    return


@upgrade_step('cell_line', '1', '2')
def cell_line_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-207
    return
