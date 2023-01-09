from snovault import upgrade_step


@upgrade_step('access_key', '1', '2')
def access_key_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-221
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']


@upgrade_step('access_key', '2', '3')
def access_key_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-321
    if 'aliases' in value:
        value['alias'] = value['aliases']
        del value['aliases']
