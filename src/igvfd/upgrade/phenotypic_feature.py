from snovault import upgrade_step


@upgrade_step('phenotypic_feature', '1', '2')
def phenotypic_feature_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']


@upgrade_step('phenotypic_feature', '2', '3')
def phenotypic_feature_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1494
    if value['status'] in ['released', 'archived'] and 'release_timestamp' not in value:
        value['release_timestamp'] = '2024-03-06T12:34:56Z'
        notes = value.get('notes', '')
        notes += f'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'
        value['notes'] = notes.strip()


@upgrade_step('phenotypic_feature', '3', '4')
def phenotypic_feature_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2131
    apoe_carrier_enum_map = {
        '2/2': 'E2/E2',
        '2/3': 'E2/E3',
        '2/4': 'E2/E4',
        '3/3': 'E3/E3',
        '3/4': 'E3/E4',
        '4/4': 'E4/E4'
    }
    if 'quality' in value:
        if value['quality'] in apoe_carrier_enum_map.keys():
            old_enum = value['quality']
            value['quality'] = apoe_carrier_enum_map[old_enum]
            notes = value.get('notes', '')
            notes += f'This object\'s quality was {old_enum} but is now replaced by {apoe_carrier_enum_map[old_enum]}.'
            value['notes'] = notes.strip()
