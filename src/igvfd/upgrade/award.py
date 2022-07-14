from snovault import upgrade_step


@upgrade_step('award', '1', '2')
def award_1_2(value, system):
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
