from snovault import upgrade_step


@upgrade_step('publication', '1', '2')
def publication_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-221
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']


@upgrade_step('publication', '2', '3')
def publication_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-802
    if 'identifiers' in value:
        value['publication_identifiers'] = value['identifiers']
        del value['identifiers']


@upgrade_step('publication', '3', '4')
def publication_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']
