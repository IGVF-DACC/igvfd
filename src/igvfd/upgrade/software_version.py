from snovault import upgrade_step


@upgrade_step('software_version', '1', '2')
def software_version_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-802
    if 'references' in value:
        value['publication_identifiers'] = value['references']
        del value['references']


@upgrade_step('software_version', '2', '3')
def software_version_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1163
    notes = value.get('notes', '')
    if 'version' in value:
        version = value['version'].split('.')
        if len(version) != 3:
            notes += f' Version property (previous content: {value["version"]}) is no longer valid, default value of v0.0.1 has been assigned.'
            value['version'] = 'v0.0.1'
        elif not(version[0].startswith('v')):
            version[0] = 'v'+version[0]
            version = '.'.join(version)
            value['version'] = version
    new_notes = notes.strip()
    value['notes'] = new_notes


@upgrade_step('software_version', '3', '4')
def software_version_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']


@upgrade_step('software_version', '4', '5')
def software_version_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1494
    if value['status'] in ['released', 'archived'] and 'release_timestamp' not in value:
        value['release_timestamp'] = '2024-03-06T12:34:56Z'
        notes = value.get('notes', '')
        notes += f'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'
        value['notes'] = notes.strip()


@upgrade_step('software_version', '5', '6')
def software_version_5_6(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1686
    software_note = ''
    version_note = ''
    lab_note = ''
    award_note = ''
    if 'software' not in value:
        value['software'] = '/software/graphreg/'
        software_note = 'This software version lacked a link to a software and has been upgraded to link to /software/graphreg/ as a placeholder.'
    if 'version' not in value:
        value['version'] = 'v1.0.0'
        version_note = 'This software version lacked a version and has been upgraded to v1.0.0 as a placeholder.'
    if 'lab' not in value:
        value['lab'] = '/labs/j-michael-cherry/'
        lab_note = 'This software version lacked a lab and has been upgraded to /labs/j-michael-cherry/ as a placeholder.'
    if 'award' not in value:
        value['award'] = '/awards/HG012012/'
        award_note = 'This software version lacked an award and has been upgraded to /awards/HG012012/ as a placeholder.'
    merged_note = ' '.join([x for x in [software_note, version_note, lab_note, award_note] if x != ''])
    notes = value.get('notes', '')
    notes += merged_note
    if notes:
        value['notes'] = notes.strip()
