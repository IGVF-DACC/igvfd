from snovault import upgrade_step


@upgrade_step('user', '1', '2')
def user_1_2(value, system):
    if 'submits_for' in value:
        if len(value['submits_for']) == 0:
            del value['submits_for']
    if 'groups' in value:
        if len(value['groups']) == 0:
            del value['groups']
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
