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
