from snovault import upgrade_step


@upgrade_step('award', '1', '2')
def award_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-221
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']


@upgrade_step('award', '2', '3')
def award_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-321
    if 'pi' in value:
        value['pis'] = value['pi']
        del value['pi']
