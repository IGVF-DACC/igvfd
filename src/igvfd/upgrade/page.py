from snovault import upgrade_step


@upgrade_step('page', '1', '2')
def page_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-221
    if 'news_keywords' in value:
        if len(value['news_keywords']) == 0:
            del value['news_keywords']
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']


@upgrade_step('page', '2', '3')
def page_2_3(value, system):
    if 'news' in value:
        del value['news']
    if 'news_excerpt' in value:
        del value['news_excerpt']
    if 'news_keywords' in value:
        del value['news_keywords']
    if 'layout' in value:
        if 'rows' in value['layout']:
            del value['layout']['rows']
        if 'blocks' in value['layout']:
            richtextblocks = [block for block in value['layout']['blocks'] if block['@type'] == 'richtextblock']
            for block in richtextblocks:
                block.update({'@type': 'markdown', 'direction': 'ltr'})
            value['layout']['blocks'] = richtextblocks


@upgrade_step('page', '3', '4')
def page_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']


@upgrade_step('page', '4', '5')
def page_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1494
    if value['status'] in ['released', 'archived'] and 'release_timestamp' not in value:
        value['release_timestamp'] = '2024-03-06T12:34:56Z'
        notes = value.get('notes', '')
        notes += f'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'
        value['notes'] = notes.strip()
