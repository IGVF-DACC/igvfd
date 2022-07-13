from snovault import upgrade_step


@upgrade_step('cell_line', '1', '2')
def cell_line_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-207
    return
