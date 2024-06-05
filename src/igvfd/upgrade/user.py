from snovault import upgrade_step


@upgrade_step('user', '1', '2')
def user_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-221
    if 'submits_for' in value:
        if len(value['submits_for']) == 0:
            del value['submits_for']
    if 'groups' in value:
        if len(value['groups']) == 0:
            del value['groups']
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']


@upgrade_step('user', '2', '3')
def user_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']


@upgrade_step('user', '3', '4')
def user_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1533
    if 'viewing_groups' in value:
        if len(value['viewing_groups']) < 1:
            del value['viewing_groups']


@upgrade_step('user', '4', '5')
def user_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1671
    if ' ' in value.get('email'):
        new_email = value['email'].replace(' ', '')
        notes = value.get('notes')
        notes = notes + f'This user previously specified {value.get('email')} as its email, but was upgraded to {new_email}.'
        value['email'] = new_email
    return
