from snovault import upgrade_step


@upgrade_step('biomarker', '1', '2')
def biomarker_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-649
    value['status'] = 'in progress'
