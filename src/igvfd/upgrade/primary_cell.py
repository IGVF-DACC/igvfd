from snovault import upgrade_step


@upgrade_step('primary_cell', '1', '2')
def primary_cell_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-207
    return
