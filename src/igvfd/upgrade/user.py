from snovault import upgrade_step
import re


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
    email = value.get('email')
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    if not (re.fullmatch(pattern, email)):
        new_email = 'replace_this_email@email.com'
        value['email'] = new_email
        notes = value.get('notes', '')
        notes = f'{notes} This user previously specified {email} as its email, but was upgraded to {new_email} as it violated the regular expression introduced.'
    return


@upgrade_step('user', '5', '6')
def user_5_6(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1942
    value['email'] = value['email'].lower()
