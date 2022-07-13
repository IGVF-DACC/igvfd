from snovault import upgrade_step


@upgrade_step('rodent_donor', '1', '2')
def rodent_donor_1_2(value, system):
    if 'parents' in value:
        if len(value['parents']) == 0:
            del value['parents']
    if 'external_resources' in value:
        if len(value['external_resources']) == 0:
            del value['external_resources']
