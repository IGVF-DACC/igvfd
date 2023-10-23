from snovault import upgrade_step


@upgrade_step('analysis_step', '1', '2')
def analysis_step_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1212
    if 'parents' in value and len(value['parents']) == 0:
        del value['parents']
