from snovault import upgrade_step


@upgrade_step('lab', '1', '2')
def lab_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-221
    if 'awards' in value:
        if len(value['awards']) == 0:
            del value['awards']
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
