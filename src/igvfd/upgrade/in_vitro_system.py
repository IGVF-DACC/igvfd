from snovault import upgrade_step


@upgrade_step('in_vitro_system', '4', '5')
def in_vitro_system_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-471
    if value['classification'] == 'differentiated tissue':
        value['classification'] = 'organoid'
