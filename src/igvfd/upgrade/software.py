from snovault import upgrade_step


@upgrade_step('software', '1', '2')
def software_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-802
    if 'references' in value:
        value['publication_identifiers'] = value['references']
        del value['references']


@upgrade_step('software', '2', '3')
def software_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']


@upgrade_step('software', '3', '4')
def software_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1494
    if value['status'] == 'released' or value['status'] == 'archived':
        if 'release_timestamp' not in value:
            value['release_timestamp'] == '2024-03-06T12:34:56Z'
            notes = value.get('notes', '')
            notes += f'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'
            value['notes'] = notes.strip()
