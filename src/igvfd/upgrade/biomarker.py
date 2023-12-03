from snovault import upgrade_step


@upgrade_step('biomarker', '1', '2')
def biomarker_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-649
    value['status'] = 'in progress'


@upgrade_step('biomarker', '2', '3')
def biomarker_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']
