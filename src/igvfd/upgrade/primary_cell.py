from snovault import upgrade_step


@upgrade_step('primary_cell', '2', '3')
def primary_cell_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-210
    return


@upgrade_step('primary_cell', '1', '2')
def primary_cell_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-207
    return

@upgrade_step('primary_cell', '2', '3')
def primary_cell_2_3(value, system):
    if 'treatments' in value and len(value['treatments']) == 0:
        del value['treatments']
    if 'donors' in value and len(value['donors']) == 0:
        del value['donors']
    if 'dbxrefs' in value and len(value['dbxrefs']) == 0:
        del value['dbxrefs']
