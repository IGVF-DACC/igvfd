from snovault import upgrade_step


@upgrade_step('software', '1', '2')
def software_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-802
    if 'references' in value:
        value['publication_identifiers'] = value['references']
        del value['references']
