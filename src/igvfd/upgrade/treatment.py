from snovault import upgrade_step


@upgrade_step('treatment', '1', '2')
def treatment_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-221
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
    if 'documents' in value:
        if len(value['documents']) == 0:
            del value['documents']


@upgrade_step('treatment', '2', '3')
def treatment_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-292
    return
