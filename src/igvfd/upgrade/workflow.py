from snovault import upgrade_step


@upgrade_step('workflow', '1', '2')
def workflow_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-802
    if 'references' in value:
        value['publication_identifiers'] = value['references']
        del value['references']


@upgrade_step('workflow', '2', '3')
def workflow_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']


@upgrade_step('workflow', '3', '4')
def workflow_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1494
    if value['status'] in ['released', 'archived', 'revoked'] and 'release_timestamp' not in value:
        value['release_timestamp'] = '2024-03-06T12:34:56Z'
        notes = value.get('notes', '')
        notes += f'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'
        value['notes'] = notes.strip()


@upgrade_step('workflow', '4', '5')
def workflow_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1789
    if 'publication_identifiers' in value:
        del value['publication_identifiers']


@upgrade_step('workflow', '5', '6')
def workflow_5_6(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2719
    if 'workflow_version' in value:
        version_old = str(value['workflow_version'])
        value['workflow_version'] = f'v{version_old}.0.0'
