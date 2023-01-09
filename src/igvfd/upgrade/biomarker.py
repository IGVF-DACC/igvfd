from snovault import upgrade_step


@upgrade_step('biomarker', '1', '2')
def biomarker_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-321
    if 'aliases' in value:
        value['alias'] = value['aliases']
        del value['aliases']
    if 'synonyms' in value:
        value['synonym'] = value['synonyms']
        del value['synonyms']
