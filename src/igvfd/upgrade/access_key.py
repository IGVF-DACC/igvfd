from snovault import upgrade_step


@upgrade_step('access_key', '1', '2')
def access_key_1_2(value, system):
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
