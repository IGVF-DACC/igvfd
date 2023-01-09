from snovault import upgrade_step


@upgrade_step('human_genomic_variant', '1', '2')
def variant_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-321
    if 'aliases' in value:
        value['alias'] = value['aliases']
        del value['aliases']
