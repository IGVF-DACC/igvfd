from snovault import upgrade_step


@upgrade_step('software', '1', '2')
def software_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-321
    if 'aliases' in value:
        value['alias'] = value['aliases']
        del value['aliases']
    if 'references' in value:
        value['reference'] = value['references']
        del value['references']
