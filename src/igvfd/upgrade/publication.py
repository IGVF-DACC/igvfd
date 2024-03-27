from snovault import upgrade_step


@upgrade_step('publication', '1', '2')
def publication_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-221
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']


@upgrade_step('publication', '2', '3')
def publication_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-802
    if 'identifiers' in value:
        value['publication_identifiers'] = value['identifiers']
        del value['identifiers']


@upgrade_step('publication', '3', '4')
def publication_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']


@upgrade_step('publication', '4', '5')
def publication_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1494
    if value['status'] in ['released', 'archived'] and 'release_timestamp' not in value:
        value['release_timestamp'] = '2024-03-06T12:34:56Z'
        notes = value.get('notes', '')
        notes += f'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'
        value['notes'] = notes.strip()


@upgrade_step('publication', '5', '6')
def publication_5_6(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1533
    if 'published_by' in value:
        if len(value['published_by']) < 1:
            del value['published_by']
