from snovault import upgrade_step


@upgrade_step('document', '1', '2')
def document_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-221
    if 'urls' in value:
        if len(value['urls']) == 0:
            del value['urls']
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']


@upgrade_step('document', '2', '3')
def document_2_3(value, system):
    if 'description' in value:
        if value['description'] == '':
            value['description'] = 'Default upgrade text: please add details about document in description.'


@upgrade_step('document', '3', '4')
def document_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1494
    if value['status'] in ['released', 'archived'] and 'release_timestamp' not in value:
        value['release_timestamp'] = '2024-03-06T12:34:56Z'
        notes = value.get('notes', '')
        notes += f'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'
        value['notes'] = notes.strip()
