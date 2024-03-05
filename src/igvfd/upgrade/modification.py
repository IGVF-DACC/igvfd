from snovault import upgrade_step


@upgrade_step('modification', '1', '2')
def modification_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-729
    if 'cas_species' not in value:
        value['notes'] = (value.get(
            'notes', '') + 'For upgrade, cas_species has been automatically designated as Streptococcus pyogenes (Sp), follow up with associated lab to check if upgrade is valid.').strip()
        value['cas_species'] = 'Streptococcus pyogenes (Sp)'


@upgrade_step('modification', '2', '3')
def modification_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-895
    # Source property is pluralized
    if 'source' in value:
        value['sources'] = [value['source']]
        del value['source']


@upgrade_step('modification', '3', '4')
def modification_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']


@upgrade_step('modification', '4', '5')
def modification_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1494
    if value['status'] == 'released' or value['status'] == 'archived':
        if 'release_timestamp' not in value:
            value['release_timestamp'] = '2024-03-06T12:34:56Z'
            notes = value.get('notes', '')
            notes += f'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'
            value['notes'] = notes.strip()
