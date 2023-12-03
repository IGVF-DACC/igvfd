from snovault import upgrade_step


@upgrade_step('phenotypic_feature', '1', '2')
def phenotypic_feature_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']
