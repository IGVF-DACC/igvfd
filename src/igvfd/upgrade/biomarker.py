from snovault import upgrade_step


@upgrade_step('biomarker', '1', '2')
def biomarker_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-649
    value['status'] = 'in progress'


@upgrade_step('biomarker', '2', '3')
def biomarker_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']


@upgrade_step('biomarker', '3', '4')
def biomarker_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1494
    if value['status'] in ['released', 'archived'] and 'release_timestamp' not in value:
        value['release_timestamp'] = '2024-03-06T12:34:56Z'
        notes = value.get('notes', '')
        notes += f'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'
        value['notes'] = notes.strip()
