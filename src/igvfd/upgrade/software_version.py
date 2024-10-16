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
        elif not (version[0].startswith('v')):
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
    # https://igvf.atlassian.net/browse/IGVF-1789
    if 'publication_identifiers' in value:
        del value['publication_identifiers']


@upgrade_step('software_version', '6', '7')
def software_version_6_7(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1949
    if 'downloaded_url' in value:
        value['source_url'] = value['downloaded_url']
        del value['downloaded_url']
